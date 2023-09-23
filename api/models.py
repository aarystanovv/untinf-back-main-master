from django.db import models
from mongoengine import Document, fields


class Question(Document):
    question = fields.StringField(max_length=100000, null=True)
    content = fields.URLField(null=True)
    task = fields.StringField(max_length=10000)
    taskContent = fields.URLField(null=True)
    options = fields.ListField(fields.StringField(max_length=10000))
    answers = fields.ListField(fields.StringField(max_length=10000))
    type = fields.StringField(max_length=1000)
    topic = fields.ListField(fields.StringField(max_length=10000))
    format = fields.StringField(max_length=1000)

    def __str__(self):
        return self.question
