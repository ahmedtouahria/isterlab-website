from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin,TabularInline
# Register your models here.

class ServiceFAQAdmin(TabularInline):
    model = ServiceFAQ

class SolutionFAQAdmin(TabularInline):
    model = SolutionFAQ

class ServiceAdmin(ModelAdmin):
    model = Service
    list_display = ['name']
    inlines = [ServiceFAQAdmin]
class SolutionsAdmin(ModelAdmin):
    model = Solution
    list_display = ['name']
    inlines = [SolutionFAQAdmin]
class BrandAdmin(ModelAdmin):
    model = Brand
    list_display = ['name']

admin.site.register(Solution,SolutionsAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Coverage)
admin.site.register(Brand,BrandAdmin)