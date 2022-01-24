from rest_framework import serializers
from .models import QuestionUpvote, Room, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer', 'created_at']


# class AddUpdateAnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Answer
#         fields = ['answer']

#     def save(self, **kwargs):
#         id = self.context['id']
#         question_id = self.context['question_id']
#         answer = self.validated_data['answer']

#         answer, created = Answer.objects.update_or_create(
#             pk=id,
#             question_id=question_id,
#             defaults={'answer': answer}
#         )

#         self.instance = answer
#         return answer

class SimpleQuestionUpvoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionUpvote
        fields = ['student_id']

# class DeleteQuestionUpvoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = QuestionUpvote
#         fields = ['question_id', 'student_id']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'upvotes',
                  'upvoted', 'created_at', 'answers']

    answers = AnswerSerializer(many=True)
    upvotes = serializers.SerializerMethodField(
        method_name='get_upvotes'
    )
    upvoted = serializers.SerializerMethodField(
        method_name='check_upvoted'
    )

    def get_upvotes(self, question):
        return question.question_upvotes.count()

    def check_upvoted(self, question):
        user_id = self.context.get('user_id')
        for question_upvote in list(question.question_upvotes.all()):
            if user_id == question_upvote.user_id:
                return True
        return False
    # upvotes = serializers.SerializerMethodField(
    #     method_name='get_upvotes'
    # )

    # def get_upvotes(self, question):
    #     return question.question_upvotes.count()


# class AddUpdateQuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Question
#         fields = ['question']

#     def save(self, **kwargs):
#         print(self.context)
#         id = self.context['id']
#         room_id = self.context['room_id']
#         question = self.validated_data['question']

#         question, created = Question.objects.update_or_create(
#             pk=id,
#             room_id=room_id,
#             defaults={'question': question}
#         )

#         self.instance = question
#         return question


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['module', 'questions', 'num_lost', 'is_lost']

    questions = QuestionSerializer(many=True)
    num_lost = serializers.SerializerMethodField(
        method_name='get_num_lost'
    )
    is_lost = serializers.SerializerMethodField(
        method_name='check_lost'
    )

    def get_num_lost(self, room):
        return room.lost_users.count()

    def check_lost(self, room):
        user_id = self.context.get('user_id')
        for lost_user in list(room.lost_users.all()):
            if user_id == lost_user.user_id:
                return True
        return False


class SimpleRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'module']


# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ['id', 'email', '']


# class UnitSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Unit
#         fields = ['rooms']

#     rooms = SimpleRoomSerializer(many=True)
    # students = StudentSerializer(many=True)
