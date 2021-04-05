from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Address(models.Model):
    add_line_1 = models.CharField(max_length=255)
    add_line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.IntegerField()
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.add_line_1


class Brand(models.Model):
    brand = models.CharField(max_length=255)

    def __str__(self):
        return self.brand


class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category


class Product(models.Model):
    name = models.CharField(max_length=255)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    description = models.TextField(max_length=255)
    product_image = models.ImageField(max_length=255, upload_to="product_images/", null=True, blank=True)
    price = models.IntegerField(default=100)

    def __str__(self):
        return str(self.name)


class Profile(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile_no = models.IntegerField()
    alter_mobile_no = models.IntegerField()
    address = models.ManyToManyField(Address, )

    def __str__(self):
        return str(self.mobile_no)


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    is_purchase = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
