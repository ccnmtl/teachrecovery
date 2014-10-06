from django.contrib import admin
from pagetree.models import Hierarchy

from teachrecovery.main.models import UserModule


def section_hierarchy(obj):
    return obj.section.hierarchy.name
section_hierarchy.short_description = 'Hierarchy'


class UserModuleAdmin(admin.ModelAdmin):
    list_display = ['user', section_hierarchy, 'is_allowed']

admin.site.register(UserModule, UserModuleAdmin)
admin.site.register(Hierarchy)
