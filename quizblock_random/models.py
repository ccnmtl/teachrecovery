from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import smart_str
from pagetree.models import PageBlock, Section
from pagetree.reports import ReportableInterface, ReportColumnInterface
from quizblock.models import *
from django.http import HttpResponse


class QuizRandom(Quiz):
    display_name = "Quiz Random"
    template_file = "quizblock_random/quizblock_random.html"
    quiz_name = models.CharField(max_length=50)
    
    def pageblock(self):
        return self.pageblocks.all()[0]

    def quiz(self):
        return self.quiz.all()[0]

    def edit_form(self):
        class EditForm(forms.Form):
            description = forms.CharField(widget=forms.widgets.Textarea(),
                                          initial=self.description)
            rhetorical = forms.BooleanField(initial=self.rhetorical)
            allow_redo = forms.BooleanField(initial=self.allow_redo)
            show_submit_state = forms.BooleanField(
                initial=self.show_submit_state)
            alt_text = ("<a href=\"" + reverse("edit-quiz-random", args=[self.id])
                        + "\">manage questions/answers</a>")
        return EditForm()

    def get_question(self):
        return 

    @classmethod
    def create(self, request):
        return QuizRandom.objects.create(
            quiz_name = request.POST.get('label'),
            )


class RandomQuizSection(models.Model):
    display_name = "Random Quiz"
    section = models.ForeignKey(Section)
    user = models.ForeignKey(User)
    quiz_current = models.NullBooleanField(null=True)

    @classmethod
    def create(self, section, user):
        return RandomQuizSection.objects.create(
            section_id = section.id,
            user_id = user.id
        )


class QuestionUserLock(models.Model):
    quiz = models.ForeignKey(QuizRandom)
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    random_quiz = models.ForeignKey(RandomQuizSection, null=True, blank=True)
    question_used = models.NullBooleanField(null=True)
    question_current = models.NullBooleanField(null=True)


    def set_question_user_lock(self, question, user):
        try:
            current_question = QuestionUserLock.objects.filter(quiz_id=question.quiz.id).get(question_current = True)
            qid = current_question.question_id
            question  = Question.objects.get(id=qid)
            return question
            
        except QuestionUserLock.DoesNotExist:
            rand_int = randint(0, set_len-1)
            q = question_set[rand_int]
            return q


    @classmethod
    def create(self, question, user, rq):
        return QuestionUserLock.objects.create(
            quiz_id = question.quiz.id, 
            question_id = question.id, 
            user_id = user.id,
            random_quiz_id = rq.id
            )