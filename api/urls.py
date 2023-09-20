from django.urls import include, path
from rest_framework import routers

from api import views
from api.views import QuestionViewSet

router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('question_variants/', views.generate_question_variants, name='question_variants'),
]
