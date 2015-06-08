from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView
from pagetree.generic.views import PageView, EditView
from pagetree.generic.views import generic_edit_page
from pagetree.generic.views import generic_instructor_page
from pagetree.models import UserPageVisit, Hierarchy
from teachrecovery.main.models import UserModule, ResourcePage
from django.http.response import HttpResponseNotFound
from django.shortcuts import render


class LoggedInMixinSuperuser(object):
    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixinSuperuser, self).dispatch(*args, **kwargs)


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get(self, request):
        if not request.user.is_anonymous():
            ums = UserModule.objects.filter(
                user=request.user).order_by('hierarchy__id')
            um_info = list()
            for um in ums:
                root = um.hierarchy.section_set.all().first()
                module = root.get_first_child()
                slug = module.slug
                name = slug.replace('-', ' ')
                um_info.append([um, name])
            context = dict(user_modules=um_info)
            return render(request, self.template_name, context)

        context = dict(user_modules=None)
        return render(request, self.template_name, context)


def has_responses(section):
    quizzes = [p.block() for p in section.pageblock_set.all()
               if hasattr(p.block(), 'needs_submit')
               and p.block().needs_submit()]
    return quizzes != []


class DynamicHierarchyMixin(object):
    def dispatch(self, *args, **kwargs):
        name = kwargs.pop('hierarchy_name', None)
        if name is None:
            msg = "No hierarchy named %s found" % name
            return HttpResponseNotFound(msg)
        else:
            self.hierarchy_name = name
            self.hierarchy_base = Hierarchy.objects.get(name=name).base_url
        return super(DynamicHierarchyMixin, self).dispatch(*args, **kwargs)


class RestrictedModuleMixin(object):
    def dispatch(self, *args, **kwargs):
        hierarchy = Hierarchy.objects.get(name=self.hierarchy_name)
        um = UserModule.objects.filter(user=self.request.user,
                                       hierarchy=hierarchy,
                                       is_allowed=True)
        if len(um) < 1:
            return HttpResponse("you don't have permission")
        return super(RestrictedModuleMixin, self).dispatch(*args, **kwargs)


class TeachRecoveryPageView(LoggedInMixin,
                            DynamicHierarchyMixin,
                            RestrictedModuleMixin,
                            PageView):
    template_name = "pagetree/page.html"
    gated = True

    def get_extra_context(self, **kwargs):
        hierarchy = self.section.hierarchy
        rps = ResourcePage.objects.filter(hierarchy=hierarchy)
        menu = []
        visits = UserPageVisit.objects.filter(user=self.request.user,
                                              status='complete')
        visit_ids = visits.values_list('section__id', flat=True)
        previous_unlocked = True
        for section in self.root.get_descendants():
            unlocked = section.id in visit_ids
            item = {
                'id': section.id,
                'url': section.get_absolute_url(),
                'label': section.label,
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
        return {'menu': menu, 'page_status': status, 'resource_pages': rps}


class TeachRecoveryEditView(LoggedInMixinSuperuser,
                            DynamicHierarchyMixin,
                            EditView):
    template_name = "pagetree/edit_page.html"


@login_required
def pages_save_edit(request, hierarchy_name, path):
    # do auth on the request if you need the user to be logged in
    # or only want some particular users to be able to get here
    return generic_edit_page(request, path, hierarchy=hierarchy_name)


@login_required
def instructor_page(request, hierarchy_name, path):
    return generic_instructor_page(request, path, hierarchy=hierarchy_name)
