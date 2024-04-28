from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=100)
    description= models.TextField(max_length=1000)
    category= models.CharField(max_length=20)
    dueDate= models.DateTimeField()

    def __str__(self):
        return f"Tasks of {self.user.username}"