from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Question
import json



class QuestionListView(APIView):

    def get(self, request):
        all_questions = Question.objects

        selected_questions = all_questions[:35]

        serialized_questions = []
        for question in selected_questions:
            serialized_question = {
                "id": str(question.pk),
                "question": question.question,
                "content": question.content,
                "task": question.task,
                "taskContent": question.taskContent,
                "options": question.options,
                "type": question.type,
                "topic": question.topic,
                "format": question.format
            }
            serialized_questions.append(serialized_question)

        response_data = {"questions": serialized_questions}
        return Response(response_data)

    @extend_schema(
        request="gs",
        description="Add question multiple or simple for multiple 8 options, for simple questions 5 options. Answer for multiple 1-3, simple must be only 1 answer",
        examples=[
            OpenApiExample(
                name="Simple Successful request",
                value={
                    "question": "What is the capital of France?",
                    "content": "https://raw.githubusercontent.com/guinnod/photo-base/main/13.jpg",
                    "task": "Find the capital",
                    "taskContent": "https://raw.githubusercontent.com/guinnod/photo-base/main/14.jpg",
                    "options": ["Paris", "London", "Berlin", "Astana", "Moscow"],
                    "answers": ["Paris"],
                    "type": "simple",
                    "topic": ["Geography", "Tourism"],
                    "format": "text"
                },
                description="Simple question post",
            ),
            OpenApiExample(
                name="Multiple Successful request",
                value={
                    "question": "What is the capitals of France, Kazakhstan?",
                    "content": "https://raw.githubusercontent.com/guinnod/photo-base/main/13.jpg",
                    "task": "Find the capital",
                    "taskContent": "https://raw.githubusercontent.com/guinnod/photo-base/main/14.jpg",
                    "options": ["Paris", "London", "Berlin", "Astana", "Moscow", "Ulan-Bator", "Kiev", "America"],
                    "answers": ["Paris", "Astana"],
                    "type": "simple",
                    "topic": ["Geography", "Tourism"],
                    "format": "text"
                },
                description="Multiple answer question post",
            ),
        ]
    )
    def post(self, request):

        try:
            data = request.data

            question = Question(
                question=data.get('question'),
                content=data.get('content'),
                task=data.get('task'),
                taskContent=data.get('taskContent'),
                options=data.get('options'),
                answers=data.get('answers'),
                type=data.get('type'),
                topic=data.get('topic'),
                format=data.get('format')
            )

            question.save()

            return Response({'message': 'Question added successfully'})

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
