import random

from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .serializers import TestSerializer, QuestionSerializer, OptionSerializer

from .models import Test, Question, Option

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    #permission_classes = [permissions.IsAdminUser]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    #permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Question.objects.all()
        topic = self.request.query_params.get('test__topic')
        question_type = self.request.query_params.get('question_type')
        form = self.request.query_params.get('test__form')

        if topic:
            queryset = queryset.filter(test__topic=topic)

        if question_type:
            queryset = queryset.filter(question_type=question_type)

        if form:
            queryset = queryset.filter(test__form=form)

        return queryset


class OptionViewSet(viewsets.ModelViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    #permission_classes = [permissions.IsAdminUser]

    def list(self, request, *args, **kwargs):
        all_options = list(Option.objects.all())
        random.shuffle(all_options)
        serializer = self.get_serializer(all_options, many=True)
        return Response(serializer.data)