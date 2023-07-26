from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser,models.Model):


    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        db_table = 'df_user'