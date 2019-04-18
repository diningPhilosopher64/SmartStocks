from django.db import models
from django.contrib.auth.models import User
 
class Financials(models.Model):
    user = models.ForeignKey(User,to_field="username",on_delete=models.DO_NOTHING)
    stocks_owned=models.TextField(blank=True)
    account_num = models.IntegerField(default=0,blank=False)
    balance=models.DecimalField(decimal_places=2,max_digits=9)
    def __str__(self):
        return self.user
