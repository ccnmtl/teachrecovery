from annoying.decorators import render_to
from pagetree.helpers import get_hierarchy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
#from django.views.generic.base import View, TemplateView
from pagetree.generic.views import generic_edit_page
from pagetree.generic.views import generic_instructor_page
from django.contrib.auth.decorators import login_required, user_passes_test
from pagetree.generic.views import PageView, EditView
from pagetree.models import UserPageVisit
from django.utils.decorators import method_decorator
from teachrecovery.main.models import UserModule

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
    if request.user.is_anonymous():
        return dict()
    else:
        return HttpResponseRedirect('/pages/')


def has_responses(section):
    quizzes = [p.block() for p in section.pageblock_set.all()
               if hasattr(p.block(), 'needs_submit')
               and p.block().needs_submit()]
    return quizzes != []


class ViewPage(LoggedInMixin, PageView):
    template_name = "pagetree/page.html"
    hierarchy_name = "main"
    hierarchy_base = "/pages/"
    gated = True


    def gate_check(self, user):
        user = self.request.user
        section = self.section
        module = self.section.get_module()
        if section.id == module.id:
            return None

        if not self.get_gated():
            return None
        # we need to check that they have visited all previous pages
        # first
        allow, first = self.gate_check_module(user, self.section)
        #import pdb
        #pdb.set_trace()
        if not allow:
            # redirect to the first one that they need to visit
            return HttpResponseRedirect(first.get_absolute_url())

    def gate_check_module(self, user, section):
            """ return bool, section tuple for whether the user
            has visited every section previous to this one and
            which is the first that they need to visit if that's
            not the case """
            if not user:
                # no user: the important thing is just that we deny access
                return False, self

            # otherwise, let's start at the beginning and check each
            depth_first_traversal = section.get_annotated_list(
                parent=section.get_module())

            # prep a list of all the visits for this user
            upvs = [upv.section.id
                    for upv in list(UserPageVisit.objects.filter(user=user))
                    if upv.status == 'complete']
            for (i, (s, ai)) in enumerate(depth_first_traversal):
                # skip the root
                if s.is_root():
                    continue
                if s.id == section.id:
                    # we've reached the current section. That
                    # means they're good to go.
                    return True, None
                else:
                    if s.id not in upvs:
                        # uh oh. found a page that they haven't visited
                        # need to send them there first
                        return False, s
            # went through the entire list of sections without finding
            # the current section?!
            assert False, "current section not found in traversal"

    def get(self, request, path):
        allow_redo = False
        needs_submit = self.section.needs_submit()
        if needs_submit:
            allow_redo = self.section.allow_redo()
        self.upv.visit()
        instructor_link = has_responses(self.section)
        context = dict(
            section=self.section,
            module=self.module,
            needs_submit=needs_submit,
            allow_redo=allow_redo,
            is_submitted=self.section.submitted(request.user),
            modules=self.root.get_children(),
            root=self.section.hierarchy.get_root(),
            instructor_link=instructor_link,
        )

        context.update(self.get_extra_context())
        try:
            um = UserModule.objects.get(
                section_id=self.module.id,
                user_id=self.request.user.id)
            if um.is_allowed:
                return render(request, self.template_name, context)
            else:
                return HttpResponse("you don't have permission")
        except (ValueError, ObjectDoesNotExist):
                return HttpResponse("you don't have permission")

    def get_extra_context(self, **kwargs):
        menu = []
        visits = UserPageVisit.objects.filter(user=self.request.user,
                                              status='complete')
        visit_ids = visits.values_list('section__id', flat=True)
        previous_unlocked = True
        for section in self.root.get_descendants():
            unlocked = section.id in visit_ids
            section_module = section.get_module()

            item = {
                'id': section.id,
                'url': section.get_absolute_url(),
                'label': section.label,
                'section_module': section_module,
                'depth': section.depth,
                'slug': section.slug,
                'disabled': not(previous_unlocked or section.id in visit_ids)
            }
            if section.depth == 3 and section.get_children():
                item['toggle'] = True
            menu.append(item)
            previous_unlocked = unlocked
            uv = self.section.get_uservisit(self.request.user)
            try:
                status = uv.status
            except AttributeError:
                status = 'incomplete'
        return {'menu': menu, 'page_status': status}


class EditPage(LoggedInMixinSuperuser, EditView):
    template_name = "pagetree/edit_page.html"
    hierarchy_name = "main"
    hierarchy_base = "/pages/"


@login_required
def pages_save_edit(request, path):
    # do auth on the request if you need the user to be logged in
    # or only want some particular users to be able to get here
    path = request.GET['p']
    h = teach_recovery_get_hierarchy(request, path)
    return generic_edit_page(request, path, hierarchy=h)


@login_required
def instructor_page(request, path):
    # do any additional auth here
    h = teach_recovery_get_hierarchy(request, path)
    return generic_instructor_page(request, path, hierarchy=h)


@login_required
def teach_recovery_get_hierarchy(request, path):
    h = get_hierarchy("main", "/pages/")
    return h
