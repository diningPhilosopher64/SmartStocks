from django.db import models
from django.db.models.signals import post_save
from iex import Stock as Stock_iex


# Create your models here.


class Stock(models.Model):

    # Present
    stock_name = models.CharField(max_length=20, blank=False, null=False)

    # Get from iex. WIll retrieve in save() function
    company_name = models.CharField(max_length=100, blank=True)

    # Company information
    table_data = models.TextField(blank=True, null=False)

    #Company Description
    description = models.TextField(blank=True, null=True)


    #Checks if downloaded from wiki
    is_downloaded = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.company_name = Stock_iex(self.stock_name).company()['companyName']
        super().save(*args, **kwargs)  # Call the "real" save() method.


