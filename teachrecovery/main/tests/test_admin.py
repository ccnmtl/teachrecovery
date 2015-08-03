from django.test import TestCase
from teachrecovery.main.admin import hierarchy


class TestHierarchy(TestCase):
    def test_hierarchy(self):
        class Dummy(object):
            pass

        obj = Dummy()
        obj.hierarchy = Dummy()
        obj.hierarchy.name = "this is it"
        self.assertEqual(hierarchy(obj), "this is it")
