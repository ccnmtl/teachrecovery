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


class QuizRandom(Quiz):
	quiz = generic.GenericRelation(Quiz)
	content_type = models.ForeignKey(
        ContentType,
        verbose_name=('Quiz Random'),
        null=True,
        blank=True,
    )

	object_id = models.PositiveIntegerField(
    	verbose_name=('related object'),
    	null=True,
   	)
    

	display_name = "Quiz Random"
	template_file = "quizblock_random/quizblock_random.html"
	quiz_name = models.CharField(max_length=50)

	content_object = generic.GenericForeignKey('content_type', 'object_id')