from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# from .models import Room, Question, Answer
from .models import Question, QuestionUpvote, Room, EnrolledRoom
# from .serializers import RoomSerializer, QuestionSerializer, AddUpdateQuestionSerializer, AnswerSerializer, AddUpdateAnswerSerializer
from .serializers import RoomSerializer, SimpleRoomSerializer


# class UnitViewSet(ListModelMixin, GenericViewSet):
#     def get_queryset(self):
#         user_id = self.request.user.id
#         student = Student.objects.get(user_id=user_id)
#         return Unit.objects.filter(students=student.id).prefetch_related('rooms')
#     serializer_class = UnitSerializer
#     permission_classes = [IsAuthenticated]

# def retrieve(self, request, *args, **kwargs):
#     instance = self.get_object()
#     serializer = self.get_serializer(instance)
#     return Response(serializer.data)

# class UnitDetail(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk):
#         student = Student.objects.get(user_id=request.user.id)
#         queryset = Unit.objects.filter(
#             students=student.id
#         ).prefetch_related('rooms')
#         serializer = UnitSerializer(queryset, many=True)
#         return Response(serializer.data)


class RoomViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Room.objects.prefetch_related('questions__answers').prefetch_related('questions__question_upvotes').all()

        enrolled_rooms_queryset = EnrolledRoom.objects.filter(
            user_id=self.request.user.id
        )
        return Room.objects.filter(
            enrolled_rooms__in=enrolled_rooms_queryset
        ).prefetch_related('questions__answers').prefetch_related('questions__question_upvotes')

    def get_serializer_class(self):
        if self.action == 'list':
            return SimpleRoomSerializer
        return RoomSerializer

    def get_serializer_context(self):
        return {
            'user_id': self.request.user.id,
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def retrieve(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            serializer = self.get_serializer(self.get_object())
            return Response(serializer.data)

        is_authorized = EnrolledRoom.objects.filter(
            user_id=request.user.id
        ).exists()

        if not is_authorized:
            return Response(
                data={
                    'code': 'student_unauthorized',
                    'detail': 'User is not authorized to enter this room'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)


# class QuestionUpvoteViewSet(CreateModelMixin, DestroyModelMixin, GenericViewSet):
#     queryset = QuestionUpvote.objects.all()
#     serializer_class = QuestionUpvoteSerializer


# class QuestionViewSet(ModelViewSet):
#     def get_queryset(self):
#         return Question.objects.filter(room=self.kwargs['room_pk']).prefetch_related('answers').order_by('created_at')

#     def get_serializer_class(self):
#         if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'PATCH':
#             return AddUpdateQuestionSerializer
#         return QuestionSerializer

#     def get_serializer_context(self):
#         room_id = self.kwargs['room_pk']
#         id = self.kwargs.get('pk')
#         return {'room_id': room_id, 'id': id}


# class AnswerViewSet(ModelViewSet):
#     def get_queryset(self):
#         return Answer.objects.filter(question=self.kwargs['question_pk']).order_by('created_at')

#     def get_serializer_class(self):
#         if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'PATCH':
#             return AddUpdateAnswerSerializer
#         return AnswerSerializer

#     def get_serializer_context(self):
#         question_id = self.kwargs['question_pk']
#         id = self.kwargs.get('pk')
#         return {'question_id': question_id, 'id': id}
