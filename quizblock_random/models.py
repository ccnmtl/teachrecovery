from datetime import datetime
from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import smart_str
from pagetree.models import PageBlock
from pagetree.reports import ReportableInterface, ReportColumnInterface
from quizblock.models import *
from django.http import HttpResponse


class QuizRandom(Quiz):
    quiz = generic.GenericRelation(Quiz)
    pageblock = generic.GenericRelation(PageBlock)
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



    @classmethod
    def create(self, request):
        return QuizRandom.objects.create(
        quiz_name = request.POST.get('label'),
    )