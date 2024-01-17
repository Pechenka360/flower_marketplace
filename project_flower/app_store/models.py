from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.html import escape, mark_safe
from django.db.models import F


# Create your models here.


class Category(MPTTModel):
    title = models.CharField(max_length=150, verbose_name='Наименование категории')
    slug = models.SlugField(null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Родитель',
        related_name='subcategories'
    )
    image = models.ImageField(upload_to='photos/categories/', null=True, blank=True,
                              verbose_name='Изображение')

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Seller(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование продавца')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'


class Brand(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование бренда')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование продукта')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория',
                                 related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(null=True, blank=True, verbose_name='Описание товара')
    slug = models.SlugField(null=True)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, verbose_name='Продавец', null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, verbose_name='Бренд', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def get_first_photo(self):
        if self.images:
            try:
                return self.images.all()[0].image.url
            except:
                return '-'
        else:
            return '-'

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Color(models.Model):
    title = models.CharField(max_length=150, verbose_name='Цвет')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'


class SizeCategory(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование категории размеров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория размеров'
        verbose_name_plural = 'Категории размеров'


class Size(models.Model):
    parent = models.ForeignKey(SizeCategory, on_delete=models.CASCADE, verbose_name='Категория размера',
                               related_name='attribute')
    title = models.CharField(max_length=150, verbose_name='Размер')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Цвет')
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Размер')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Цена')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество на складе')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'Вариация продукта'
        verbose_name_plural = 'Вариации продукта'


class Photo(models.Model):
    image = models.ImageField(upload_to='photos/products/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def image_tag(self):
        return mark_safe('<img src="%s" height="75" />' % self.image.url)

    image_tag.short_description = 'Миниатюра'

    def __str__(self):
        return f'{self.product.title}'

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
