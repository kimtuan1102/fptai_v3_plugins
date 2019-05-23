from survey_plugins.models import Survey, Question, Choice, Answer, UserAnswer
from rest_framework import serializers


class ChoiceSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    question = serializers.ReadOnlyField(source='question.id')

    class Meta:
        model = Choice
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    token = serializers.ReadOnlyField()
    # survey = serializers.ReadOnlyField(source='survey.token')
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('token', 'choices', 'question', 'created')


class SurveySerializer(serializers.ModelSerializer):
    token = serializers.ReadOnlyField()
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Survey
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Answer
        fields = ('question', 'answer', 'created')


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = ('user', 'question', 'answer', 'created')
