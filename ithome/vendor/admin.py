from django.contrib import admin

# 後方新增 你所建立的 "類別名稱"，這裡我的名稱是VendorAdmin
from .models import Vendor, Food, VendorAdmin

# Register your models here.
# 將管理者類別 VendorAdmin 填至該類別後方
# admin.site.register(Vendor, VendorAdmin)
# admin.site.register(Food)