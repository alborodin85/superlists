from django.test import TestCase

class SmokeTest(TestCase):
    '''Тест на токсичность'''

    def test_bad_math(self):
        self.assertEqual(1+1, 3);
