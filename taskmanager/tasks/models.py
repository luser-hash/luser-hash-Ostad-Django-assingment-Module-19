from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    STATUS_CHOICE = [
        ('pending', 'Pending'),
        ('in progress', 'In progress'),
        ('completed', 'Completed'),
    ]

    PRIORITY_CHOICE = [
        ('low', 'Low'),
        ('medium', 'MEDIUM'),
        ('high', 'High'),
    ]
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, 
                                 null=True, blank=True, related_name='tasks')
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICE, 
                              default='pending')
    priority = models.CharField(max_length=30, choices=PRIORITY_CHOICE, 
                                default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_at = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, 
                              related_name='tasks')

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name