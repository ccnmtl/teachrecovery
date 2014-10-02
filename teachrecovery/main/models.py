from django.db import models
from pagetree.generic.views import PageView, EditView

class PageViewExtend(PageView):
    display_name = "Page View Extend"
    hierarchy = models.CharField(max_length=255)