#from django.views.generic.base import TemplateView
from annoying.decorators import render_to
from django.http import HttpResponseRedirect
from pagetree.generic.views import PageView, EditView
from pagetree.helpers import get_hierarchy
from pagetree.generic.views import generic_view_page
from pagetree.generic.views import generic_edit_page
from pagetree.generic.views import generic_instructor_page
from django.contrib.auth.decorators import login_required, user_passes_test
#from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
#from django import forms


class LoggedInMixinSuperuser(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinSuperuser, self).dispatch(*args, **kwargs)


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


@render_to('main/index.html')
def index(request):
    return dict()


def page(request, path):
    # do auth on the request if you need the user to be logged in
    # or only want some particular users to be able to get here
    h = get_hierarchy("main", "/pages/")
    return generic_view_page(request, path, hierarchy=h)


@login_required
def pages_save_edit(request, path):
    # do auth on the request if you need the user to be logged in
    # or only want some particular users to be able to get here
    #import pdb
    #pdb.set_trace()
    path = request.GET['p']
    h = get_hierarchy("main", "/pages/")
    return generic_edit_page(request, path, hierarchy=h)


@login_required
def edit_page(request, path):
    # do any additional auth here
    h = get_hierarchy("main", "/pages/")
    return generic_edit_page(request, path, hierarchy=h)


@login_required
def instructor_page(request, path):
    # do any additional auth here
    h = get_hierarchy("main", "/pages/")
    return generic_instructor_page(request, path, hierarchy=h)
