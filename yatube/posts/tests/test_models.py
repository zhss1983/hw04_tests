from django.test import TestCase

from .test_setups import MySetupTestCase


class PostModelTest(TestCase, MySetupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        MySetupTestCase.setUpClass()

    def test_object_text_field(self):
        """Check __str__, it must return self.text[:15]."""
        cls = self.__class__
        result_str = cls.post.text[:15]
        self.assertEqual(result_str, str(cls.post))


class GroupModelTest(TestCase, MySetupTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        MySetupTestCase.setUpClass()

    def test_object_title_field(self):
        """Check __str__, it must return self.title."""
        cls = self.__class__
        result_str = cls.group.title
        self.assertEqual(result_str, str(cls.group))
