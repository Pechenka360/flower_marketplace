from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from .models import *


# Register your models here.


class SubcategoryInline(admin.TabularInline):
    model = Category
    fk_name = 'parent'
    prepopulated_fields = {'slug': ('title',)}
    show_change_link = True
    extra = 1

    verbose_name = 'Подкатегория'
    verbose_name_plural = 'Подкатегории'


class ProductsInline(admin.TabularInline):
    model = Product
    fk_name = 'category'
    exclude = ['description']
    fields = ['title', 'price', 'quantity', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    show_change_link = True
    extra = 1


class ProductsVariationsInline(admin.TabularInline):
    model = ProductVariation
    fk_name = 'product'
    show_change_link = True
    extra = 1


class PhotoInline(admin.TabularInline):
    model = Photo
    fk_name = 'product'
    extra = 3
    readonly_fields = ('image_tag',)


class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions', 'indented_title', 'title', 'parent', 'get_subcategories_count', 'get_products_count')
    list_display_links = ('indented_title',)
    list_filter = ('parent',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [SubcategoryInline, ProductsInline]

    def get_subcategories_count(self, obj):
        if obj.subcategories:
            return str(len(obj.subcategories.all()))
        else:
            return '0'

    def get_products_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'

    get_subcategories_count.short_description = 'Количество подкатегорий'

    get_products_count.short_description = 'Количество товаров'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'category', 'price', 'quantity', 'created_at', 'get_photo')
    list_editable = ('price', 'quantity', 'category')
    list_display_links = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'category', 'price', 'quantity', 'brand', 'created_at')

    inlines = [ProductsVariationsInline, PhotoInline]

    def get_photo(self, obj):
        if obj.images:
            try:
                return mark_safe(f'<img src="{obj.images.all()[0].image.url}" height="75">')
            except:
                return '-'
        else:
            return '-'

    get_photo.short_description = 'Миниатюра'


class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ('image_tag',)


class MyAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        return app_list


admin.site = MyAdminSite()

admin.site.register(Group)
admin.site.register(User, UserAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Seller)
admin.site.register(Brand)
admin.site.register(Product, ProductAdmin)
admin.site.register(Color)
admin.site.register(SizeCategory)
admin.site.register(Size)
admin.site.register(ProductVariation)
admin.site.register(Photo, PhotoAdmin)
