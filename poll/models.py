from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    phone=models.IntegerField(null=True)

class POll(models.Model):
    question=models.CharField(max_length=100)
    owner=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="poll")
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.question

class Choices(models.Model):
    option=models.CharField(max_length=200)
    poll_obj=models.ForeignKey(POll,on_delete=models.CASCADE,related_name="choice")

    def __str__(self):
        return self.option

class Vote(models.Model):
    poll_obj=models.ForeignKey(POll,on_delete=models.CASCADE,related_name="votes")
    choice_obj=models.ForeignKey(Choices,on_delete=models.CASCADE,related_name="votes")
    owner_obj=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="votes")
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('poll_obj','owner_obj')