from django.db import models
from django.contrib.contenttypes import generic
from django import forms
from django.contrib.auth.models import User
from pagetree.models import Section, PageBlock


class UserModule(models.Model):
    display_name = "User Module"
    user = models.ForeignKey(User)
    section = models.ForeignKey(Section)
    is_allowed = models.NullBooleanField()

    @classmethod
    def create(self, user, section):
        um = self(user_id=user.id, section_id=section.id)
        return um


class CoinGame(models.Model):
    display_name = "Coin Game"
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "coin_game/coin_game.html"

    def pageblock(self):
        return self.pageblocks.all()[0]

        @classmethod
        def create(self, request):
            return CoinGame.objects.create()

        @classmethod
        def add_form(self):
            class AddForm(forms.Form):
                display_name = self.display_name
            return AddForm()

        def edit_form(self):
            class EditForm(forms.Form):
                display_name = forms.CharField(
                    widget=forms.widgets.Textarea(),
                    default=self.display_name)
            return EditForm
