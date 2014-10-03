from django.db import models
from django.contrib.auth.models import User
from pagetree.models import Section


class UserModule(models.Model):
    display_name = "User Module"
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    is_allowed = models.NullBooleanField()

    @classmethod
    def create(self, user, section):
        um = self(user_id=user.id, section_id=section.id)
        return um
