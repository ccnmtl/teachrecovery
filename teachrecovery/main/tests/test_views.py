from django.test import TestCase
from django.test.client import Client
from pagetree.helpers import get_hierarchy
from django.contrib.auth.models import User
from teachrecovery.main.views import (
    DynamicHierarchyMixin, RestrictedModuleMixin,
    TeachRecoveryPageView,
)
from teachrecovery.main.models import UserModule


class BasicTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_root(self):
        response = self.c.get("/")
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'Columbia Log In')

    def test_smoketest(self):
        response = self.c.get("/smoketest/")
        self.assertEquals(response.status_code, 200)
        assert "PASS" in response.content


class PagetreeViewTestsLoggedOut(TestCase):
    def setUp(self):
        self.c = Client()
        self.h = get_hierarchy("main", "/pages/main/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })

    def test_page(self):
        r = self.c.get("/pages/main/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_edit_page(self):
        r = self.c.get("/pages/main/edit/section-1/")
        self.assertEqual(r.status_code, 302)

    def test_instructor_page(self):
        r = self.c.get("/pages/main/instructor/section-1/")
        self.assertEqual(r.status_code, 302)


class PagetreeViewTestsLoggedIn(TestCase):
    def setUp(self):
        self.c = Client()
        self.h = get_hierarchy("main", "/pages/main/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        self.u = User.objects.create(username="testuser", is_superuser=True)
        self.u.set_password("test")
        self.u.save()
        self.c.login(username="testuser", password="test")

    def test_page(self):
        r = self.c.get("/pages/main/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_edit_page(self):
        r = self.c.get("/pages/main/edit/section-1/")
        self.assertEqual(r.status_code, 200)

    def test_instructor_page(self):
        r = self.c.get("/pages/main/instructor/section-1/")
        self.assertEqual(r.status_code, 200)


class DynamicHierarchyMixinTest(TestCase):
    def test_dispatch(self):
        d = DynamicHierarchyMixin()
        r = d.dispatch(hierarchy_name=None)
        self.assertEqual(r.status_code, 404)
        self.assertTrue("No hierarchy named" in r.content)


class P(object):
    def dispatch(self, *args, **kwargs):
        return True


class DummyRequest(object):
    def __init__(self, user):
        self.user = user


class M(RestrictedModuleMixin, P):
    def __init__(self, user, hierarchy_name):
        self.hierarchy_name = hierarchy_name
        self.request = DummyRequest(user)


class RestrictedModuleMixinTest(TestCase):
    def setUp(self):
        self.h = get_hierarchy("main", "/pages/main/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        self.u = User.objects.create(username="testuser", is_superuser=True)

    def test_dispatch_denied(self):
        m = M(self.u, "main")
        r = m.dispatch()
        self.assertEqual(r.content, "you don't have permission")

    def test_dispatch_allowed(self):
        m = M(self.u, "main")
        UserModule.objects.create(user=self.u, section=self.root,
                                  is_allowed=True)
        self.assertTrue(m.dispatch())


class TeachRecoveryPageViewTest(TestCase):
    def setUp(self):
        self.h = get_hierarchy("main", "/pages/main/")
        self.root = self.h.get_root()
        self.root.add_child_section_from_dict(
            {
                'label': 'Section 1',
                'slug': 'section-1',
                'pageblocks': [],
                'children': [],
            })
        self.u = User.objects.create(username="testuser", is_superuser=True)

    def test_get_extra_content(self):
        trpv = TeachRecoveryPageView()
        trpv.request = DummyRequest(self.u)
        trpv.root = self.root
        trpv.section = self.root
        r = trpv.get_extra_context()
        self.assertTrue('menu' in r)
        self.assertTrue('page_status' in r)
        self.assertEqual(r['page_status'], 'incomplete')
