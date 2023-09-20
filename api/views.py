import random
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Question
from api.serializers import QuestionSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = Question.objects.all()
        question_list = list(queryset)
        random.shuffle(question_list)
        return question_list

    @action(detail=False, methods=['post'])
    def update_answers(self, request):
        questions = Question.objects.all()

        for question in questions:
            if not question.answers:
                question.answers = [question.answer]
            else:
                question.answers.append(question.answer)

            question.save()

        return Response(status=status.HTTP_302_FOUND, headers={'Location': '/'})


def generate_question_variants(request):
    all_questions = Question.objects.all()

    single_questions = all_questions.filter(type="single")[:20]
    context_questions = all_questions.filter(type="context")[:5]
    multiple_questions = all_questions.filter(type="multiple")[:10]

    questions = list(single_questions) + list(context_questions) + list(multiple_questions)

    questions = random.sample(questions, len(questions))


    return render(request, 'questions.html', {'questions': questions})
