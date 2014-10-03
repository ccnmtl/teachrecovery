from django.contrib import admin
from pagetree.models import Section, Hierarchy
from teachrecovery.main.models import UserModule

admin.site.register(Hierarchy)
admin.site.register(UserModule)