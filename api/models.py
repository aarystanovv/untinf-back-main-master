import uuid
from django.db import models

class Test(models.Model):
    topic = models.CharField(max_length=100)
    type_choices = (
        ('Python', 'Python'),
        ('Excel', 'Excel'),
        ('HTML5', 'HTML5'),
    )
    type = models.CharField(max_length=100, choices=type_choices)
    format_choices = (
        ('theory', 'Theory'),
        ('practice', 'Practice'),
        ('simple', 'Simple'),
    )
    format = models.CharField(max_length=100, choices=format_choices)
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.topic

class Question(models.Model):
    question = models.CharField(max_length=1000)
    content = models.URLField()
    task = models.CharField(max_length=1000)
    taskContent = models.URLField()
    type = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    answer = models.CharField(max_length=1000)
    format = models.CharField(max_length=100)
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.question

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text
