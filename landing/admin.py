from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin,TabularInline
# Register your models here.
from constance.admin import ConstanceAdmin, Config
from constance.forms import ConstanceForm
class CustomConfigForm(ConstanceForm):
      def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #... do stuff to make your settings form nice ...

class ConfigAdmin(ConstanceAdmin):
    change_list_form = CustomConfigForm
    change_list_template = 'admin/constance/change_list.html'

admin.site.unregister([Config])
admin.site.register([Config], ConfigAdmin)
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

class CovergeAdmin(ModelAdmin):
    model = Coverage

admin.site.register(Solution,SolutionsAdmin)
admin.site.register(Service,ServiceAdmin)
admin.site.register(Coverage,CovergeAdmin)
admin.site.register(Brand,BrandAdmin)
admin.site.register(FAQ)