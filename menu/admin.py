from django.contrib import admin
from .models import Category, ProductFood

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name')

class ProductFoodAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug': ('food_title',)}
    list_display = ('food_title', 'category', 'price', 'is_available', 'vendor', 'updated_at')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductFood, ProductFoodAdmin)
