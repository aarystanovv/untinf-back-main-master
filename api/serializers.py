from rest_framework import serializers
from .models import Question
from bson import ObjectId


class QuestionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    question = serializers.CharField(max_length=100000, allow_null=True)
    content = serializers.URLField(allow_null=True)
    task = serializers.CharField(max_length=10000, allow_null=True)
    taskContent = serializers.URLField(allow_null=True)
    options = serializers.ListField(child=serializers.CharField(max_length=10000))
    answers = serializers.ListField(child=serializers.CharField(max_length=10000))
    type = serializers.CharField(max_length=1000)
    topic = serializers.ListField(child=serializers.CharField(max_length=1000))
    format = serializers.CharField(max_length=1000)

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('answers', None)
        return data
