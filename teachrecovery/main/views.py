from django.views.generic.base import TemplateView
#from django.http import HttpResponseRedirect, HttpResponse
from pagetree.generic.views import PageView, EditView
from django.contrib.auth.decorators import login_required, user_passes_test
#from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
#from django import forms


# add classes for view
class IndexView(TemplateView):
    template_name = "main/index.html"


class LoggedInMixinSuperuser(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinSuperuser, self).dispatch(*args, **kwargs)


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class EditPage(LoggedInMixinSuperuser, EditView):
    template_name = "main/edit_page.html"
    hierarchy_name = "main"
    hierarchy_base = "/pages/"


class InstructorPage(LoggedInMixinSuperuser, EditView):
    template_name = "main/instructor_page.html"
    hierarchy_name = "main"
    hierarchy_base = "/"


class ViewPage(LoggedInMixin, PageView):
    template_name = "main/page.html"
    hierarchy_name = "main"
    hierarchy_base = "/pages/"
    gated = False
