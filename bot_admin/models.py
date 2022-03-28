from django.db import models
from multiselectfield import MultiSelectField


# Create your models here.
class Client(models.Model):
    user_id = models.BigIntegerField(verbose_name="user_id", primary_key=True)
    name = models.CharField(verbose_name="Имя", max_length=64)
    region = models.TextField(verbose_name="Регион")
    number = models.CharField(verbose_name="Номер телефона", max_length=13)

    def __str__(self):
        if self.name:
            return f"{self.name}  [{self.number}]"

        return f"{str(self.user_id)}  [{self.number}]"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Category(models.Model):
    category = models.CharField(verbose_name="Категория", max_length=64, unique=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)  # to_field="category"
    sub_category = models.CharField(verbose_name="Подкатегория", max_length=64, unique=True, null=True, blank=True)

    def __str__(self):
        return self.sub_category

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Brand(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)  # to_field="category"
    sub_category = models.ForeignKey(SubCategory, verbose_name="Подкатегория",
                                     on_delete=models.CASCADE, null=True, blank=True)  # to_field="sub_category"
    brand = models.CharField(verbose_name="Бренд", max_length=64)

    def __str__(self):
        return f"{self.brand} - {self.category}"

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)  # to_field="category"
    sub_category = models.ForeignKey(SubCategory, verbose_name="Подкатегория",
                                     on_delete=models.CASCADE, null=True, blank=True)  # to_field="sub_category"
    brand = models.ManyToManyField(Brand, verbose_name="Бренд")
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Описание", max_length=870, null=True, blank=True)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Order(models.Model):
    client = models.ForeignKey(Client, verbose_name="Заказчик", on_delete=models.CASCADE)
    total_check = models.FloatField(verbose_name="Итоговая сумма чека")
    complete = models.BooleanField(verbose_name="Завершенность заказа", default=False)
    order_items = models.TextField(verbose_name="Заказанные продукты")
    date_ordered = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)
    # order_items = models.ManyToManyField(OrderItem, verbose_name="Заказанные продукты")

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    client_id = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, verbose_name="Id заказа", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField(verbose_name="Количество")
    product_price = models.FloatField(verbose_name="Цена")
    total_sum = models.FloatField(verbose_name="К оплате за товар")
    date_added = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = "Продукт в корзине"
        verbose_name_plural = "Продукты в корзине"


class Contact(models.Model):
    addresses = models.TextField(verbose_name="Адреса", null=True, blank=True)
    phone_numbers = models.TextField(verbose_name="Номера телефонов", null=True, blank=True)
    locations = models.TextField(verbose_name="Ссылки локаций", null=True, blank=True)

    def __str__(self):
        return self.addresses

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"


class About_Us(models.Model):
    about_us = models.TextField(verbose_name="О нас", null=True, blank=True)

    def __str__(self):
        return self.about_us

    class Meta:
        verbose_name = "О нас"
        verbose_name_plural = "О нас"

