from cryptocurrency.client import Client
from django.test import TestCase


class APITestCase(TestCase):
    def setUp(self) -> None:
        api_key, api_secret = 1, 1
        self.client = Client(api_key, api_secret)

    def test_fetch(self):
        self.assertIsNotNone(self.client)
        order = self.client.get_order(symbol='BNBBTC')
        self.assertAlmostEquals()
