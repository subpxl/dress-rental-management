from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

class CategoryAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    pass


class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    pass

# Register your models here.
admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)