from django import template
from quizblock.models import Quiz, Question, Response, Submission
from quizblock_random.models import QuizRandom, QuestionUserLock
register = template.Library()

@register.assignment_tag
def get_questions(section, block, question, user):
	q_set = block.get_random_question_set(section, block, question, user)
	is_correct = question.is_user_correct(user)
	import pdb
	pdb.set_trace()
	return is_correct
    #return quiz_random.get_random_question(user)