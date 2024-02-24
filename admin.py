from django.contrib import admin
from .models import Categories, Subcategories, Product, CartItem
# Register your models here.
@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display=["name"]

@admin.register(Subcategories)
class SubcategoriesAdmin(admin.ModelAdmin):
    list_display=["name"]

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=["product_name","price","categories","subcategories","desc","image"]

@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display=["product","quantity","user"]


