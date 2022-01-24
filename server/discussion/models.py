from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from uuid import uuid4


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


# class Unit(models.Model):
#     code = models.CharField(max_length=255)

#     def __str__(self):
#         return self.code


# class Student(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     unit = models.ForeignKey(
#         Unit,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name='students'
#     )


class Room(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    unit = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.unit}: {self.module}'


class EnrolledRoom(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrolled_rooms'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='enrolled_rooms'
    )


class Question(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.answer


class QuestionUpvote(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='question_upvotes'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='question_upvotes'
    )

    class Meta:
        unique_together = [['user', 'question']]


class LostUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='lost_users'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='lost_users'
    )

    class Meta:
        unique_together = [['user', 'room']]
