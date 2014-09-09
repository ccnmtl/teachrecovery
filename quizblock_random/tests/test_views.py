from django.test import TestCase
from django.test.client import RequestFactory
from pagetree.tests.factories import UserFactory
from quizblock.models import Quiz, Question, Answer
from quizblock.views import EditQuizView, AddQuestionToQuizView, \
    EditQuestionView, AddAnswerToQuestionView, DeleteQuestionView, \
    DeleteAnswerView, EditAnswerView, ReorderAnswersView, ReorderQuestionsView

