from rest_framework import authentication, exceptions, HTTP_HEADER_ENCODING
from django.middleware.csrf import CsrfViewMiddleware


def get_authorization_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    return auth


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class SurveyPluginAuthentication(authentication.BaseAuthentication):
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from .models import Survey
        return Survey

    def authenticate(self, request):
        auth = get_authorization_header(request)
        model = self.get_model()
        if not auth:
            raise exceptions.AuthenticationFailed('The plugins failed to authenticate. Missing authentication token')
        if not auth.startswith("Bearer "):
            raise exceptions.AuthenticationFailed('The plugins failed to authenticate. Missing Bearer token')
        auth_token = auth.replace("Bearer ", "")
        try:
            survey = model.objects.all().get(token=auth_token)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('The plugins failed to authenticate. Invalid token')
        return None, survey.token


class QuestionPluginAuthentication(authentication.BaseAuthentication):
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from .models import Question
        return Question

    def authenticate(self, request):
        auth = get_authorization_header(request)
        model = self.get_model()
        if not auth:
            raise exceptions.AuthenticationFailed('The plugins failed to authenticate. Missing authentication token')
        if not auth.startswith("Bearer "):
            raise exceptions.AuthenticationFailed('The plugins failed to authenticate. Missing Bearer token')
        auth_token = auth.replace("Bearer ", "")
        try:
            question = model.objects.all().get(token=auth_token)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('The plugins failed to authenticate. Invalid token')
        return None, question.token
