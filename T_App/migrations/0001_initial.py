# Generated by Django 3.2.2 on 2023-03-12 12:39

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Age',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age_ct', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('amount', models.CharField(max_length=100)),
                ('payment_id', models.CharField(blank=True, max_length=300, null=True)),
                ('paid', models.BooleanField(default=False, null=True)),
                ('date', models.DateField(default=datetime.datetime.today)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='T_App.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='ecommerce/pimg')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('is_featured', models.BooleanField(default=False)),
                ('stock', models.IntegerField(default='')),
                ('color', models.CharField(default='', max_length=100)),
                ('detail', models.TextField()),
                ('age_no', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='T_App.age')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='T_App.brand')),
                ('category', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='T_App.category')),
                ('sub_category', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='T_App.sub_category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='ecommerce/Order_img')),
                ('quantity', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('total', models.CharField(max_length=1000)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='T_App.order')),
            ],
        ),
    ]
