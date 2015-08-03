from django.test import TestCase
from .factories import UserFactory, GameSubmissionFactory
from pagetree.tests.factories import ModuleFactory
from teachrecovery.main.models import (
    UserModule, CoinGame, GameSubmission)


class UserModuleTest(TestCase):
    def test_create(self):
        u = UserFactory()
        module = ModuleFactory(hname="main", base_url="/")
        um = UserModule.create(u, module.root.hierarchy)
        self.assertEqual(um.user, u)

    def test_unicode(self):
        u = UserFactory()
        module = ModuleFactory(hname="main", base_url="/")
        um = UserModule.create(u, module.root.hierarchy)
        self.assertEqual(str(um), "main")


class CoinGameTest(TestCase):
    def setUp(self):
        self.c = CoinGame.create(None)

    def test_needs_submit(self):
        self.assertTrue(self.c.needs_submit())

    def test_edit_form(self):
        e = self.c.edit_form()
        self.assertTrue('display_name' in e.base_fields)

    def test_edit(self):
        self.c.edit(dict(label="foo"), None)
        self.assertEqual(self.c.label, "foo")

    def test_submit(self):
        u = UserFactory()
        self.c.submit(u, None)
        self.assertEqual(GameSubmission.objects.filter(user=u).count(), 1)

    def test_redirect_to_self_on_submit(self):
        self.assertFalse(self.c.redirect_to_self_on_submit())

    def test_clear_user_submissions(self):
        u = UserFactory()
        self.c.submit(u, None)
        self.assertEqual(GameSubmission.objects.filter(user=u).count(), 1)
        self.c.clear_user_submissions(u)
        self.assertEqual(GameSubmission.objects.filter(user=u).count(), 0)

    def test_unlocked(self):
        u = UserFactory()
        self.assertFalse(self.c.unlocked(u))
        self.c.submit(u, None)
        self.assertTrue(self.c.unlocked(u))


class GameSubmissionTest(TestCase):
    def test_unicode(self):
        gs = GameSubmissionFactory()
        self.assertTrue(str(gs).startswith("game "))
