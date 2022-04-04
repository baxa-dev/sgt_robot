# Generated by Django 3.2.3 on 2022-03-30 19:46

from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bot_admin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand_mining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mining_brand', models.CharField(max_length=64, verbose_name='Бренд')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Category_mining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mining_category', models.CharField(max_length=64, unique=True, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Motherboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pci_slots', models.IntegerField(verbose_name='Количество слотов pci-express')),
                ('socket_type', models.CharField(max_length=64, verbose_name='Тип сокета')),
                ('pci_express', multiselectfield.db.fields.MultiSelectField(choices=[('2.0', '2.0'), ('3.0', '3.0'), ('4.0', '4.0'), ('5.0', '5.0')], max_length=15, verbose_name='Версии pci-express')),
                ('ram_type', models.CharField(choices=[('DDR2', 'DDR2'), ('DDR3', 'DDR3'), ('DDR4', 'DDR4'), ('DDR5', 'DDR5')], max_length=64, verbose_name='Тип памяти')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=870, null=True, verbose_name='Описание')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.brand_mining', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.category_mining', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Материнская плата',
                'verbose_name_plural': 'Материнские платы',
            },
        ),
        migrations.CreateModel(
            name='SSD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=870, null=True, verbose_name='Описание')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.brand_mining', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.category_mining', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'SSD',
                'verbose_name_plural': 'SSD',
            },
        ),
        migrations.CreateModel(
            name='RAM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=870, null=True, verbose_name='Описание')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.brand_mining', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.category_mining', verbose_name='Категория')),
                ('ram_type', models.ManyToManyField(to='build_mining.Motherboard', verbose_name='Тип памяти')),
            ],
            options={
                'verbose_name': 'RAM',
                'verbose_name_plural': 'RAM',
            },
        ),
        migrations.CreateModel(
            name='PowerUnit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=870, null=True, verbose_name='Описание')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.brand_mining', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.category_mining', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Блок питания',
                'verbose_name_plural': 'Блоки питания',
            },
        ),
        migrations.CreateModel(
            name='Mining_OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=64, verbose_name='Продукт')),
                ('product_quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('product_price', models.FloatField(verbose_name='Цена')),
                ('total_sum', models.FloatField(verbose_name='К оплате за товар')),
                ('product_brand', models.CharField(max_length=64, verbose_name='Бренд')),
                ('product_category', models.CharField(max_length=64, verbose_name='Категория')),
                ('pci_slots', models.IntegerField(verbose_name='Количество слотов pci-express')),
                ('socket_type', models.CharField(max_length=64, verbose_name='Тип сокета')),
                ('pci_express', models.CharField(max_length=64, verbose_name='Версии pci-express')),
                ('ram_type', models.CharField(max_length=64, verbose_name='Тип памяти')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_admin.client', verbose_name='Клиент')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot_admin.order', verbose_name='Id заказа')),
            ],
            options={
                'verbose_name': 'Майнинг-Сборка пользователя',
                'verbose_name_plural': 'Майнинг-Сборки пользователя',
            },
        ),
        migrations.CreateModel(
            name='GPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=870, null=True, verbose_name='Описание')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.brand_mining', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.category_mining', verbose_name='Категория')),
                ('pci_express', models.ManyToManyField(max_length=64, to='build_mining.Motherboard', verbose_name='Версии pci-express')),
            ],
            options={
                'verbose_name': 'Видеокарта',
                'verbose_name_plural': 'Видеокарты',
            },
        ),
        migrations.CreateModel(
            name='CPU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=870, null=True, verbose_name='Описание')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.brand_mining', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.category_mining', verbose_name='Категория')),
                ('socket_type', models.ManyToManyField(to='build_mining.Motherboard', verbose_name='Тип сокета')),
            ],
            options={
                'verbose_name': 'Процессор',
                'verbose_name_plural': 'Процессоры',
            },
        ),
        migrations.CreateModel(
            name='Cooler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='', verbose_name='Фото')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Название')),
                ('description', models.TextField(blank=True, max_length=870, null=True, verbose_name='Описание')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.brand_mining', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.category_mining', verbose_name='Категория')),
                ('socket_type', models.ManyToManyField(to='build_mining.Motherboard', verbose_name='Тип сокета')),
            ],
            options={
                'verbose_name': 'Кулер',
                'verbose_name_plural': 'Кулеры',
            },
        ),
        migrations.AddField(
            model_name='brand_mining',
            name='mining_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build_mining.category_mining', verbose_name='Категория'),
        ),
    ]
