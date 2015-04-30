from django.db import models
from datetime import datetime
from django.contrib.contenttypes import generic
from django import forms
from django.contrib.auth.models import User
from pagetree.models import Hierarchy, PageBlock


class UserModule(models.Model):
    display_name = "User Module"
    user = models.ForeignKey(User)
    hierarchy = models.ForeignKey(Hierarchy, default=1, verbose_name="Course")
    is_allowed = models.NullBooleanField()

    def __unicode__(self):
        return u'%s' % (self.hierarchy.name)

    @classmethod
    def create(self, user, hierarchy):
        um = self(user_id=user.id, hierarchy_id=hierarchy.id)
        return um


class CoinGame(models.Model):
    display_name = "Coin Game"
    pageblocks = generic.GenericRelation(PageBlock)
    template_file = "coin_game/coin_game.html"
    show_submit_state = models.BooleanField(default=True)
    allow_redo = models.BooleanField(default=True)

    @classmethod
    def create(self, request):
        return CoinGame.objects.create()

    @classmethod
    def add_form(self):
        class AddForm(forms.Form):
            display_name = self.display_name
        return AddForm()

    def needs_submit(self):
        return True

    def edit_form(self):
        class EditForm(forms.Form):
            display_name = forms.CharField(
                widget=forms.widgets.Textarea(),
                initial=self.display_name)
        return EditForm

    def edit(self, vals, files):
        self.label = vals.get('label', '')
        self.save()

    def submit(self, user, data):
            GameSubmission.objects.create(game=self, user=user)

    def redirect_to_self_on_submit(self):
        return False

    def clear_user_submissions(self, user):
        GameSubmission.objects.filter(user=user, game=self).delete()

    def unlocked(self, user):
        # meaning that the user can proceed *past* this one,
        # not that they can access this one. careful.
        return GameSubmission.objects.filter(game=self, user=user).count() > 0


class GameSubmission(models.Model):
    game = models.ForeignKey(CoinGame)
    user = models.ForeignKey(User)
    submitted = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "game %d submission by %s at %s" % (self.game.id,
                                                   unicode(self.user),
                                                   self.submitted)
