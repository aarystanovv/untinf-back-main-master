from django.urls import include, path
from rest_framework import routers
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.views import *


urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(
            template_name="swagger-ui.html", url_name="schema"
        ),
        name="swagger-ui",
    ),
    path('questions/', QuestionListView.as_view()),
]
