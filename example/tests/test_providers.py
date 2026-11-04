# Django
from django.test import override_settings

# AA Example
from example.providers import esi
from example.tests import NoSocketsTestCase


class TestEsiClient(NoSocketsTestCase):
    @override_settings(DEBUG=False)
    def test_client_loads_with_debug_disabled(self):
        # when
        client = esi.client
        # then
        self.assertTrue(hasattr(client.Status, "GetStatus"))
