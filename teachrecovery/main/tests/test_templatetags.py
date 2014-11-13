from django.test import TestCase
from teachrecovery.main.templatetags.accessible import (
    submitted, SubmittedNode)


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
    def submitted(self, u):
        return u


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
