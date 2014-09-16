from django import template
from quizblock.models import Quiz, Question, Response, Submission
from quizblock_random.models import QuizRandom, QuestionUserLock
from random import randint
register = template.Library()

@register.assignment_tag
def random_question(question_set, user):
    set_len = len(question_set)
    for question in question_set:
        try:
            current_question = QuestionUserLock.objects.filter(quiz_id=question.quiz.id).get(question_current = True)
            qid = current_question.question_id
            question  = Question.objects.get(id=qid)
            return question
            
        except QuestionUserLock.DoesNotExist:
            rand_int = randint(0, set_len-1)
            q = question_set[rand_int]
            return q