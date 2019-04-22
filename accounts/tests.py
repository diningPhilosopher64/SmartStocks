from django.test import SimpleTestCase 
from django.urls import reverse, resolve
from .views import *

class TestUrls(SimpleTestCase):

    def test_index_url_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func,index)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func,login)
    
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func,register)

    def test_allusers_url_resolves(self):
        url = reverse('all_users')
        self.assertEquals(resolve(url).func,all_users)

    def test_user_details_url_resolves(self):
        url = reverse('user_details')
        self.assertEquals(resolve(url).func,user_details)

    def test_edit_user_url_resolves(self):
        url = reverse('edit',args=['some_username'])
        self.assertEquals(resolve(url).func,edit)

