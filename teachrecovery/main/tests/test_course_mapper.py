from unittest import TestCase
from teachrecovery.main.course_mapper import CourseMapper


class CourseMapperTest(TestCase):
    def test_single_affil(self):
        cm = CourseMapper()
        cm.map(None, ['crs-1'])
        # still need to determine what the actual outcome will be
