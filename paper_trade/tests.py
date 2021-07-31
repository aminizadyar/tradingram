from django.test import TestCase


class APITestCase(TestCase):
    def setUp(self) -> None:
        pass

    def test_fetch(self):
        self.assertEqual(1, 1)
