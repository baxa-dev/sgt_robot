from bot_admin.models import *
from django.db import models
from multiselectfield import MultiSelectField


# Create your models here.
class Category_mining(models.Model):
    mining_category = models.CharField(verbose_name="Категория", max_length=64, unique=True)

    def __str__(self):
        return self.mining_category

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


pci_express_choices = (('2.0', '2.0'), ('3.0', '3.0'), ('4.0', '4.0'), ('5.0', '5.0'))
ram_type_choices = (('DDR2', 'DDR2'), ('DDR3', 'DDR3'), ('DDR4', 'DDR4'), ('DDR5', 'DDR5'))


class Brand_mining(models.Model):
    mining_category = models.ForeignKey(Category_mining, verbose_name="Категория", on_delete=models.CASCADE)
    mining_brand = models.CharField(verbose_name="Бренд", max_length=64)

    def __str__(self):
        return f"{self.mining_brand} - {self.mining_category}"

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"


class Motherboard(models.Model):
    pci_slots = models.IntegerField(verbose_name="Количество слотов pci-express")  # number of slots for videocards
    socket_type = models.CharField(verbose_name="Тип сокета", max_length=64)  # CPU: socket type
    # pci_express = models.CharField(verbose_name="Версия pci-express", max_length=64)  # GPU: pci-express version
    pci_express = MultiSelectField(verbose_name="Версии pci-express", choices=pci_express_choices)
    ram_type = models.CharField(verbose_name="Тип памяти", max_length=64, choices=ram_type_choices)
    category = models.ForeignKey(Category_mining, verbose_name="Категория", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand_mining, verbose_name="Бренд", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Описание", max_length=870, null=True, blank=True)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return f"{self.name} | сокет - {self.socket_type} | версии pci-express - {self.pci_express} | " \
               f"тип памяти - {self.ram_type}"

    class Meta:
        verbose_name = "Материнская плата"
        verbose_name_plural = "Материнские платы"


class CPU(models.Model):
    # motherboard = models.ManyToManyField(Motherboard, verbose_name="Поддерживаемые материнские платы")
    socket_type = models.ManyToManyField(Motherboard, verbose_name="Тип сокета")
    category = models.ForeignKey(Category_mining, verbose_name="Категория", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand_mining, verbose_name="Бренд", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Описание", max_length=870, null=True, blank=True)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.socket_type}"

    class Meta:
        verbose_name = "Процессор"
        verbose_name_plural = "Процессоры"


class GPU(models.Model):
    # motherboard = models.ManyToManyField(Motherboard, verbose_name="Поддерживаемые материнские платы")
    pci_express = models.ManyToManyField(Motherboard, verbose_name="Версии pci-express", max_length=64)
    # pci_express = MultiSelectField(choices=pci_express_choices)
    category = models.ForeignKey(Category_mining, verbose_name="Категория", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand_mining, verbose_name="Бренд", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Описание", max_length=870, null=True, blank=True)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.pci_express}"

    class Meta:
        verbose_name = "Видеокарта"
        verbose_name_plural = "Видеокарты"


class SSD(models.Model):
    # motherboard = models.ManyToManyField(Motherboard, verbose_name="Поддерживаемые материнские платы")
    category = models.ForeignKey(Category_mining, verbose_name="Категория", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand_mining, verbose_name="Бренд", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Описание", max_length=870, null=True, blank=True)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.brand}"

    class Meta:
        verbose_name = "SSD"
        verbose_name_plural = "SSD"


class RAM(models.Model):
    # motherboard = models.ManyToManyField(Motherboard, verbose_name="Поддерживаемые материнские платы")
    ram_type = models.ManyToManyField(Motherboard, verbose_name="Тип памяти")
    category = models.ForeignKey(Category_mining, verbose_name="Категория", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand_mining, verbose_name="Бренд", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Описание", max_length=870, null=True, blank=True)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.ram_type}"

    class Meta:
        verbose_name = "RAM"
        verbose_name_plural = "RAM"


class Cooler(models.Model):
    # motherboard = models.ManyToManyField(Motherboard, verbose_name="Поддерживаемые материнские платы")
    socket_type = models.ManyToManyField(Motherboard, verbose_name="Тип сокета")
    category = models.ForeignKey(Category_mining, verbose_name="Категория", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand_mining, verbose_name="Бренд", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Описание", max_length=870, null=True, blank=True)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.socket_type}"

    class Meta:
        verbose_name = "Кулер"
        verbose_name_plural = "Кулеры"


class PowerUnit(models.Model):
    # motherboard = models.ManyToManyField(Motherboard, verbose_name="Поддерживаемые материнские платы")
    category = models.ForeignKey(Category_mining, verbose_name="Категория", on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand_mining, verbose_name="Бренд", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Фото")
    name = models.CharField(verbose_name="Название", max_length=64, unique=True)
    description = models.TextField(verbose_name="Описание", max_length=870, null=True, blank=True)
    price = models.FloatField(verbose_name="Цена", null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.brand}"

    class Meta:
        verbose_name = "Блок питания"
        verbose_name_plural = "Блоки питания"


class Mining_OrderItem(models.Model):
    client_id = models.ForeignKey(Client, verbose_name="Клиент", on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, verbose_name="Id заказа", on_delete=models.CASCADE)
    product_name = models.CharField(verbose_name="Продукт", max_length=64)
    product_quantity = models.PositiveIntegerField(verbose_name="Количество")
    product_price = models.FloatField(verbose_name="Цена")
    total_sum = models.FloatField(verbose_name="К оплате за товар")
    product_brand = models.CharField(verbose_name="Бренд", max_length=64)
    product_category = models.CharField(verbose_name="Категория", max_length=64)
    pci_slots = models.IntegerField(verbose_name="Количество слотов pci-express")
    socket_type = models.CharField(verbose_name="Тип сокета", max_length=64)
    pci_express = models.CharField(verbose_name="Версии pci-express", max_length=64)
    ram_type = models.CharField(verbose_name="Тип памяти", max_length=64)
    date_added = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)

    def __str__(self):
        return str(self.product_name)

    class Meta:
        verbose_name = "Майнинг-Сборка пользователя"
        verbose_name_plural = "Майнинг-Сборки пользователя"
