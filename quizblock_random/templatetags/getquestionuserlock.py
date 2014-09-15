from django import template
from quizblock.models import Quiz, Question, Response, Submission
from quizblock_random import QuizRandom, QuestionUserLock
register = template.Library()

@register.simple_tag
def random_question(question, user):
    import pdb
    pdb.set_trace()