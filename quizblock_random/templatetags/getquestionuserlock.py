from django import template
from quizblock.models import Quiz, Question, Response, Submission
from quizblock_random.models import QuizRandom, QuestionUserLock
from random import randint
register = template.Library()

@register.assignment_tag
def random_question(question_set, user):
    set_len = len(question_set)
    rand_int = randint(0, set_len-1)
    for question in question_set:
        if (question.user_responses(user)):
            try:
                qul = QuestionUserLock.objects.filter(
                quiz_id=question.quiz.id).get(question_current = True, question_used=False, user_id = user.id)
                qul.question_current = False
                qul.save()
                import pdb
                pdb.set_trace()
            except QuestionUserLock.DoesNotExist:
                pass

        try:
            current_question = QuestionUserLock.objects.filter(
                quiz_id=question.quiz.id).get(question_current = True, user_id = user.id)
            qid = current_question.question_id
            question  = Question.objects.get(id=qid)
            return question
            
        except QuestionUserLock.DoesNotExist:
            
            question = question_set[rand_int]
            qul = QuestionUserLock.create(question, user)
            qul.question_current = True
            qul.question_used = False
            qul.save()
            return question