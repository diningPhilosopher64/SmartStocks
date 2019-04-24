from django.test import SimpleTestCase 
from django.urls import reverse, resolve
from .views import *


class TestUrls(SimpleTestCase):
    def test_news_url_resolves(self):
        url = reverse('stocknews',args=['some_stock_name'])
        self.assertEquals(resolve(url).func, stocknews)


