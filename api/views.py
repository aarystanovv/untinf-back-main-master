import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .models import Question
import json


class QuestionListView(APIView):

    def get(self, request):
        all_questions = list(Question.objects)
        random.shuffle(all_questions)

        simple_questions = []
        multiple_choice_questions = []

        for question in all_questions:
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

            if question.type == "simple" and len(simple_questions) < 25:
                simple_questions.append(serialized_question)
            elif question.type == "multiple" and len(multiple_choice_questions) < 10:
                multiple_choice_questions.append(serialized_question)

            if len(simple_questions) == 25 and len(multiple_choice_questions) == 10:
                break

        response_data = {"questions": simple_questions + multiple_choice_questions}
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


class QuestionCheckAPIView(APIView):
    score_mapping = {
        # {1}(correct_ans),{2}(select_correct_ans),{3}(select_incorrect_ans): (score)
        (3, 3, 0): 2,
        (3, 2, 1): 1,
        (3, 2, 0): 1,
        (2, 2, 0): 2,
        (2, 2, 1): 1,
        (2, 1, 0): 1,
        (2, 1, 1): 1,
        (1, 1, 0): 2,
        (1, 1, 1): 1,
    }

    @extend_schema(
        request="ww",
        examples=[
            OpenApiExample(
                name="Submit test",
                value=[
                    {"id": "650ec192065c71759465d03b",
                     "answers": ["1000"]
                     },
                    {"id": "650ec192065c71759465d03c",
                     "answers": ["1000", "300"]
                     }
                ],
            ),
        ]
    )
    def post(self, request):
        data = request.data
        question_ids = [item['id'] for item in data]

        questions = Question.objects(id__in=question_ids)
        question_dict = {str(question.id): question for question in questions}

        test = []
        score = 0

        for question_data in data:
            question_id = str(question_data["id"])
            question_obj = question_dict.get(question_id)

            if not question_obj:
                continue

            user_answers = set(question_data["answers"])
            correct_answers = set(question_obj.answers)

            if question_obj.type == "simple":
                score_value = 1 if user_answers == correct_answers else 0
            else:
                selected_correct_ans = 0
                selected_incorrect_ans = 0
                for ans in user_answers:
                    if ans in correct_answers:
                        selected_correct_ans += 1
                    else:
                        selected_incorrect_ans += 1

                score_value = self.score_mapping.get(
                    (len(correct_answers), selected_correct_ans, selected_incorrect_ans), 0)

            score += score_value

            test.append({
                "id": question_id,
                "score": score_value,
                "answers": list(user_answers),
                "correct_answers": list(correct_answers)
            })

        return Response({
            "test": test,
            "score": score
        })
