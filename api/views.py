import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from .extend_schemas import *
import json

from .serializers import QuestionSerializer


class QuestionListView(APIView):

    def get(self, request):
        all_questions = list(Question.objects)
        random.shuffle(all_questions)

        simple_questions = []
        multiple_choice_questions = []

        for question in all_questions:

            if question.type == "simple" and len(simple_questions) < 25:
                simple_questions.append(question)
            elif question.type == "multiple" and len(multiple_choice_questions) < 10:
                multiple_choice_questions.append(question)

            if len(simple_questions) == 25 and len(multiple_choice_questions) == 10:
                break

        data = simple_questions + multiple_choice_questions

        serializer = QuestionSerializer(data, many=True)
        return Response({"questions": serializer.data})

    @question_post_extend_schema
    def post(self, request):
        try:
            data = request.data

            required_fields = ['question', 'options', 'format', 'answers', 'type']
            for field in required_fields:
                if field not in data:
                    return Response({'error': f'Missing required field: {field}'}, status=status.HTTP_400_BAD_REQUEST)

            if data.get('type') not in ['simple', 'multiple']:
                return Response({'error': 'Question "type" should be multiple or simple'},
                                status=status.HTTP_400_BAD_REQUEST)

            question = QuestionSerializer(data=data)
            question.is_valid(raise_exception=True)

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

    @questions_check_post_extend_schema
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
