from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from survey_plugins.models import Survey,Question,Choice,Answer,UserAnswer
from .serializers import SurveySerializer,QuestionSerializer,ChoiceSerializer,AnswerSerializer,UserAnswerSerializer
from .authentication import SurveyPluginAuthentication, QuestionPluginAuthentication
from rest_framework import permissions
import binascii
import os
from rest_framework import status


def generate_token():
    return binascii.hexlify(os.urandom(20)).decode()


class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (permissions.IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(token=generate_token(), questions=[])


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = (SurveyPluginAuthentication,)

    def perform_create(self, serializer):
        survey = Survey.objects.get(token=self.request.auth)
        serializer.save(token=generate_token(), survey=survey)

    def get_queryset(self):
        question = Question.objects.all().filter(survey_id=self.request.auth)
        return question


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    authentication_classes = (QuestionPluginAuthentication,)

    def perform_create(self, serializer):
        question = Question.objects.get(token=self.request.auth)
        serializer.save(id=generate_token(), question=question)

    def get_queryset(self):
        choices = Choice.objects.all().filter(question_id=self.request.auth)
        return choices


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    authentication_classes = (SurveyPluginAuthentication,)

    def perform_create(self, serializer):
        survey = Survey.objects.get(token=self.request.auth)
        serializer.save(id=generate_token(), survey=survey)

    def get_queryset(self):
        answer = Answer.objects.all().filter(survey_id=self.request.auth)
        return answer


class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    authentication_classes = (SurveyPluginAuthentication,)
    
    def perform_create(self, serializer):
        survey = Survey.objects.get(token=self.request.auth)
        serializer.save(id=generate_token(), survey=survey)

    def get_queryset(self):
        user_answer = UserAnswer.objects.all().filter(survey_id=self.request.auth)
        return user_answer

