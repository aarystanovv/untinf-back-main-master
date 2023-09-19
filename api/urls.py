from .views import QuestionViewSet, TestViewSet, OptionViewSet
from django.urls import include, path
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'tests', TestViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]