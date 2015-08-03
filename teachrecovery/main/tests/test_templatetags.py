from django.test import TestCase
from teachrecovery.main.templatetags.accessible import (
    submitted, SubmittedNode, is_module, is_from_another_module)


class DummyToken(object):
    def __init__(self, f):
        self.contents = f

    def split_contents(self):
        return [None, None]


class DummyParser(object):
    def __init__(self, nt=None):
        self.nt = nt

    def parse(self, *args, **kwargs):
        return []

    def next_token(self):
        return DummyToken(self.nt)

    def delete_first_token(self):
        pass


class TestSubmitted(TestCase):
    def test_no_else(self):
        sn = submitted(DummyParser(), DummyToken(None))
        self.assertEqual(sn.section, None)

    def test_else(self):
        sn = submitted(DummyParser("else"), DummyToken(None))
        self.assertEqual(sn.section, None)


class DummyNodeList(object):
    def __init__(self, v=None):
        self.v = v

    def render(self, context):
        return self.v


class DummyRequest(object):
    def __init__(self, user):
        self.user = user


class DummySection(object):
    def __init__(self, children=None, id=None):
        self.children = children
        self.id = id

    def submitted(self, u):
        return u

    def get_root(self):
        return self

    def get_children(self):
        return self.children or []


class TestSubmittedNode(TestCase):
    def test_render_no_context(self):
        sn = SubmittedNode('section', DummyNodeList(), DummyNodeList())
        self.assertEqual(sn.render(dict(section=None)), None)

    def test_render_with_context(self):
        sn = SubmittedNode('section', DummyNodeList("t"), DummyNodeList("f"))
        self.assertEqual(
            sn.render(
                dict(
                    section=DummySection(),
                    request=DummyRequest(True),
                )
            ),
            "t")
        self.assertEqual(
            sn.render(
                dict(
                    section=DummySection(),
                    request=DummyRequest(False),
                )
            ),
            "f")


class TestIsModule(TestCase):
    def test_no_modules(self):
        s = DummySection()
        self.assertFalse(is_module(s))

    def test_with_modules(self):
        s1 = DummySection(id=2)
        s2 = DummySection(id=1)
        s = DummySection(children=[s1, s2], id=s1.id)
        self.assertTrue(is_module(s))
        s = DummySection(children=[s2, s1], id=s1.id)
        self.assertTrue(is_module(s))


class TestIsFromAnotherModule(TestCase):
    def test_equal(self):
        s1 = DummySection(id=1)
        s2 = DummySection(id=1)
        self.assertFalse(is_from_another_module(s1, s2))

    def test_unequal(self):
        s1 = DummySection(id=1)
        s2 = DummySection(id=2)
        self.assertTrue(is_from_another_module(s1, s2))
