from django.contrib import admin
from .models import *

# Register your models here.

class BusinessAdmin(admin.ModelAdmin):
    list_display = ['firmname','verified']
    search_fields = ['gstin','firmname']
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','firmname','gstin','is_available']
    search_fields = ['name','gstin']
class RegisterAdmin(admin.ModelAdmin):
    list_display= ['name','user']
    search_fields = ['name']    

admin.site.register(Category)
admin.site.register(ChildCategory)
admin.site.register(Brand)
admin.site.register(Ad)
admin.site.register(Product,ProductAdmin)
admin.site.register(Carousel)
admin.site.register(Register,RegisterAdmin)
admin.site.register(Career)
admin.site.register(Contact)
admin.site.register(Payment)
admin.site.register(Userproduct)
admin.site.register(Business,BusinessAdmin)
