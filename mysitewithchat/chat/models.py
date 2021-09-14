# chat/models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# аккаунт пользователя
# методы создания пользователя и администратора
class MyAccountManager(BaseUserManager):

    def create_user(self, username, password = None):
        if not username:
            raise ValueError("Users must have a username.")
        user = self.model(
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password = None):
        user = self.create_user(
            username = username,
            password = password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = MyAccountManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def has_perm(self, per, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

#класс для хранения сообщений 
class ChatMessage(models.Model):

    author = models.ForeignKey(Account, related_name="author_messages", on_delete = models.CASCADE)
    content = models.TextField(blank=False,)
    timestamp = models.DateTimeField()
    visualdate = models.TextField() # поле для правильного отображения типа datetime

    def __str__(self):
        return self.author.username
    
    def last_15_messages():
        return ChatMessage.objects.order_by('timestamp').all()[:15]