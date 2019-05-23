from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token

from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    name = models.CharField(max_length=1024, default="", null=False)
    phone = models.CharField(max_length=20, default="", null=False)
    created_time = models.DateTimeField(blank=True)
    last_activity = models.DateTimeField(blank=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'user'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class Survey(models.Model):
    survey_name = models.CharField(max_length=200, blank=False)
    survey_desc = models.CharField(max_length=200, blank=True)
    token = models.CharField(_("Token"), max_length=40, primary_key=True)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    
    class Meta:
        ordering = ('created',)


class Question(models.Model):
    token = models.CharField(_("Id"), max_length=40, primary_key=True)
    question = models.CharField(max_length=1000, blank=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('created',)


class Choice(models.Model):
    id = models.CharField(_("Id"), max_length=40, primary_key=True)
    content_choice = models.CharField(max_length=1000, blank=False)
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ('created',)


class Answer(models.Model):
    id = models.CharField(_("Id"), max_length=40, primary_key=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer = models.ForeignKey(Choice, related_name='answers', on_delete= models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='answers', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ('created',)


class UserAnswer(models.Model):
    id = models.CharField(_("Id"), max_length=40, primary_key=True)
    question = models.ForeignKey(Question, related_name='u_answers', on_delete=models.CASCADE)
    answer = models.ForeignKey(Choice, related_name='u_answers', on_delete= models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='u_answers', on_delete=models.CASCADE)
    user = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ('created',)



