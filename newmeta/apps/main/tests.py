from django.test import TestCase


class Example(TestCase):

    def example_true(self):
        self.assertIs(True)
