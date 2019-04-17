from django.contrib import admin
from .models import Stock



class StockAdmin(admin.ModelAdmin):
    list_filter=["is_downloaded"]
    search_fields= ["stock_name"]


admin.site.register(Stock,StockAdmin)
