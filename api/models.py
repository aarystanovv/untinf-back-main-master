from django.db import models
import uuid

class Question(models.Model):
    question = models.CharField(max_length=100000)
    options = models.JSONField()
    content = models.URLField(null=True, blank=True)
    task = models.CharField(max_length=10000, null=True, blank=True)
    taskContent = models.URLField(null=True, blank=True)
    type = models.CharField(max_length=1000)
    topic = models.CharField(max_length=1000)
    answer = models.CharField(max_length=10000, null=True, blank=True)
    format = models.CharField(max_length=1000)
    unique_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    answers = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.question
