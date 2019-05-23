from django.conf.urls import url
from django.contrib import admin
from django.urls import include,path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

from .views import SurveyViewSet,QuestionViewSet, ChoiceViewSet, AnswerViewSet, UserAnswerViewSet

# Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Survey API",
      default_version='v2',
      description="API khảo sát",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="kimtuan1102@gmail.com"),
      license=openapi.License(name="FPT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
router = DefaultRouter()
router.register(r'survey', SurveyViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'choices', ChoiceViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'user_answer', UserAnswerViewSet)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include(router.urls)),
]
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]