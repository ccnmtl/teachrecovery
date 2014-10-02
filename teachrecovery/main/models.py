from django.db import models
from pagetree.generic.views import PageView, EditView

class PageViewExtend(PageView):
    display_name = "Page View Extend"
    hierarchy =  models.CharField(max_length=255)
	
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
        return render(request, self.template_name, context)