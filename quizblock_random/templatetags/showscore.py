from django import template
from quizblock.models import Quiz, Question, Response, Submission
from quizblock_random.models import QuizRandom, QuestionUserLock
register = template.Library()

@register.assignment_tag
def get_questions(section, block, question, user):
	block.get_random_question_set(section, block, user)
	return
    #return quiz_random.get_random_question(user)