from django.test import SimpleTestCase 
from django.urls import reverse, resolve
from .views import *

class TestUrls(SimpleTestCase):
    def test_dashboard_url_resolves(self):
        url = reverse('dashboard')
        self.assertEquals(resolve(url).func,dashboard)

    