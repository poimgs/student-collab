from datetime import timedelta
import os
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.conf import settings
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .models import EnrolledRoom, User, Room, Question, Answer


class EnrolledRoomInline(admin.TabularInline):
    model = EnrolledRoom


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'enrolled_rooms__room__unit',
                   'enrolled_rooms__room__module')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = [EnrolledRoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['unit', 'module', 'url',
                    'num_questions', 'num_students', 'created_at_sg_time']
    list_filter = ['unit', 'module']
    inlines = [EnrolledRoomInline]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            num_questions=Count('questions'),
            num_students=Count('enrolled_rooms', distinct=True)
        )

    def url(self, room):
        if os.environ['DJANGO_SETTINGS_MODULE'] == 'server.settings.dev':
            base_url = 'http://localhost:3000/'
        else:
            base_url = 'https://www.student-collab.com/'
        url = base_url + str(room.id) + '/'
        return format_html('<a href="{}">{}</a>', url, url)

    @admin.display(ordering='num_questions')
    def num_questions(self, room):
        url = (
            reverse('admin:discussion_question_changelist')
            + '?'
            + urlencode({
                'room_id': str(room.id)
            })
        )
        return format_html('<a href="{}">{} questions</a>', url, room.num_questions)

    @admin.display(ordering='num_students')
    def num_students(self, room):
        url = (
            reverse('admin:discussion_user_changelist')
            + '?'
            + urlencode({
                'enrolled_rooms__room__unit': str(room.unit)
            })
            + '&'
            + urlencode({
                'enrolled_rooms__room__module': str(room.module)
            })
        )
        return format_html('<a href="{}">{} student(s)</a>', url, room.num_students)

    @admin.display(ordering='created_at')
    def created_at_sg_time(self, room):
        return room.created_at + timedelta(hours=8)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'full_name',
                    'email', 'num_answers', 'created_at_sg_time']
    list_filter = ['room__unit', 'room__module', 'room']
    list_select_related = ['user']

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            num_answers=Count('answers')
        )

    @admin.display(ordering='num_answers')
    def num_answers(self, question):
        url = (
            reverse('admin:discussion_answer_changelist')
            + '?'
            + urlencode({
                'question_id': str(question.id)
            })
        )
        return format_html('<a href="{}">{} answers</a>', url, question.num_answers)

    def full_name(self, question):
        user = question.user
        return f'{user.first_name} {user.last_name}'

    def email(self, question):
        return question.user.email

    @admin.display(ordering='created_at')
    def created_at_sg_time(self, room):
        return room.created_at + timedelta(hours=8)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer',
                    'full_name', 'email', 'created_at_sg_time']
    list_filter = ['question__room__unit',
                   'question__room__module', 'question__room']

    def question(self, answer):
        return answer.question_id.question

    def full_name(self, answer):
        user = answer.user
        return f'{user.first_name} {user.last_name}'

    def email(self, answer):
        return answer.user.email

    @admin.display(ordering='created_at')
    def created_at_sg_time(self, room):
        return room.created_at + timedelta(hours=8)
