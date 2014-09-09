from django.test import TestCase
from quizblock.models import Quiz, Question, Answer, Submission
from quizblock.models import Response
from quizblock.templatetags.getresponse import GetQuestionResponseNode
from quizblock.templatetags.getresponse import IfAnswerInNode
from django.contrib.auth.models import User


class FakeRequest(object):
    pass

