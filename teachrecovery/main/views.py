from django.views.generic.base import TemplateView


# add classes for view
class IndexView(TemplateView):
    template_name = "main/index.html"
