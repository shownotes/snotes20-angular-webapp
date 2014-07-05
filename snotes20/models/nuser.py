from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models
from django.core.mail import send_mail
from django.core import validators
from django.utils import timezone


class NUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField('username', max_length=30, unique=True,
        validators=[validators.RegexValidator(r'^[\w.@+-]+$', 'Enter a valid username.', 'invalid')])

    email = models.EmailField('email', unique=True)
    is_staff = models.BooleanField('is_staff', default=False)
    is_active = models.BooleanField('is_active', default=True)
    date_joined = models.DateTimeField('date_joined', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        return ""

    def get_short_name(self):
        return ""

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class NUserSocialType(models.Model):
    name = models.SlugField(primary_key=True)
    human_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)


class NUserSocial(models.Model):
    user = models.ForeignKey(NUser, db_index=True, related_name="socials")
    type = models.ForeignKey(NUserSocialType, db_index=True)
    value = models.CharField(max_length=20)

    class Meta:
        unique_together = ('user', 'type')
