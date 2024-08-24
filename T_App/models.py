from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Age(models.Model):
    age_ct = models.CharField( max_length=150)

    def __str__(self):
        return self.age_ct

class Sub_Category(models.Model):
    name = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False, default='')
    sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=False, default='')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    age_no = models.ForeignKey(Age, on_delete=models.CASCADE, null=False, default='')
    image = models.ImageField(upload_to='ecommerce/pimg')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    is_featured = models.BooleanField(default=False)
    stock = models.IntegerField(default=0) # new field for stock
    color = models.CharField(max_length=100,default='')
    detail = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
   
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    address = models.TextField()
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    pincode = models.CharField(max_length=10)
    amount = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=300, null=True, blank=True)
    paid = models.BooleanField(default=False, null=True)
    date = models.DateField(default=datetime.datetime.today)
    
    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    image = models.ImageField(upload_to='ecommerce/Order_img')
    quantity = models.CharField(max_length=20)
    price = models.IntegerField()
    total = models.CharField(max_length=1000)

    def __str__(self):
        return self.order.user.username


