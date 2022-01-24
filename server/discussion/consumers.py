import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib import auth
from .models import Question, Answer, QuestionUpvote, Room, User, EnrolledRoom, LostUser
from .serializers import RoomSerializer


class DiscussionConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def check_user_authorization(self):
        if self.user.is_anonymous:
            return False
        if self.user.is_staff:
            return True

        is_authorized = EnrolledRoom.objects.filter(
            user_id=self.user.id
        ).exists()
        return is_authorized

    @database_sync_to_async
    def validate_room(self):
        try:
            Room.objects.get(pk=self.room_id)
            return True
        except Room.DoesNotExist:
            return False

    @database_sync_to_async
    def get_room_info(self):
        queryset = Room.objects.prefetch_related(
            'questions__answers'
        ).prefetch_related(
            'questions__question_upvotes'
        ).order_by(
            'questions__created_at'
        ).get(
            pk=self.room_id
        )

        serializer = RoomSerializer(queryset, context={
            'user_id': self.user.id
        })
        return serializer.data

    @database_sync_to_async
    def create_question(self, question):
        new_question = Question.objects.create(
            user_id=self.user.id,
            room_id=self.room_id,
            question=question
        )
        new_question.save()
        return new_question

    @database_sync_to_async
    def create_answer(self, question_id, answer):
        new_answer = Answer.objects.create(
            user_id=self.user.id,
            question_id=question_id,
            answer=answer
        )
        new_answer.save()
        return new_answer

    @database_sync_to_async
    def upvote_question(self, question_id):
        question_upvote, created = QuestionUpvote.objects.get_or_create(
            question_id=question_id,
            user_id=self.user.id
        )
        question_upvote.save()
        return question_upvote

    @database_sync_to_async
    def downvote_question(self, question_id):
        try:
            question_upvote = QuestionUpvote.objects.get(
                question_id=question_id,
                user_id=self.user.id
            )
            question_upvote.delete()
            return question_upvote
        except QuestionUpvote.DoesNotExist:
            print(f'{question_upvote} does not exist in database')

    @database_sync_to_async
    def user_is_lost(self):
        lost_user, created = LostUser.objects.get_or_create(
            room_id=self.room_id,
            user_id=self.user.id
        )
        lost_user.save()
        return lost_user

    @database_sync_to_async
    def user_is_not_lost(self):
        try:
            lost_user = LostUser.objects.get(
                room_id=self.room_id,
                user_id=self.user.id
            )
            lost_user.delete()
            return lost_user
        except QuestionUpvote.DoesNotExist:
            print(f'{lost_user} does not exist in database')

    async def connect(self):
        self.user = self.scope['user']
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'discussion_{self.room_id}'

        room_exists = await self.validate_room()
        authorized = await self.check_user_authorization()
        if room_exists and authorized:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['message_type']
        message = text_data_json.get('message')
        question_id = text_data_json.get('question_id')
        if message_type == 'question':
            await self.create_question(message)

        elif message_type == 'answer':
            await self.create_answer(question_id, message)

        elif message_type == 'upvote':
            await self.upvote_question(question_id)

        elif message_type == 'downvote':
            await self.downvote_question(question_id)

        elif message_type == 'is_lost':
            await self.user_is_lost()

        elif message_type == 'is_not_lost':
            await self.user_is_not_lost()

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'new_message',
        })

    async def new_message(self, event):
        updated_room_info = await self.get_room_info()
        await self.send(text_data=json.dumps(updated_room_info))
