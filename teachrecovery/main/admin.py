from django.contrib import admin
from pagetree.models import Hierarchy
from teachrecovery.main.models import UserModule


def hierarchy(obj):
    return obj.hierarchy.name

hierarchy.short_description = 'Course'


class UserModuleAdmin(admin.ModelAdmin):
    search_fields = ['user__username']
    list_display = ['user', hierarchy, 'is_allowed']

admin.site.register(UserModule, UserModuleAdmin)
admin.site.register(Hierarchy)
