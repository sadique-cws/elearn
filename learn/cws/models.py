from django.db import models
from django.conf import settings
# Create your models here.


class Category(models.Model):
    cat_title = models.CharField(max_length=200)
    slug = models.SlugField()
    cat_description = models.TextField()

    def __str__(self):
        return self.cat_title


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=200)
    duration = models.DateTimeField()
    image = models.ImageField(upload_to="course/")
    types = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    price = models.FloatField()
    discount_price = models.FloatField(null=True)
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField()
    item = models.ForeignKey(Course, on_delete=models.CASCADE)
    doc = models.DateTimeField(auto_now_add=True)

    def get_total_discount(self):
        return self.item.price - self.item.discount_price

    def get_total(self):
        return self.item.price

    def get_discount_total(self):
        return self.item.discount_price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=15)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    starting_date = models.DateTimeField()
    ordered_date = models.DateTimeField()
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey('Address',on_delete=models.SET_NULL,null=True)

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total()
        return total

    def get_payable_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_discount_total()
        if self.coupon:
            total -= self.coupon.amount
        return total

    def get_total_save_amount(self):
        return self.get_total_price() - self.get_payable_price()


class Coupon(models.Model):
    code = models.CharField(max_length=10)
    amount = models.FloatField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class Address(models.Model):
    name = models.CharField(max_length=200,null=True)
    contact = models.IntegerField()
    area = models.TextField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=200)
    pin_code = models.IntegerField()
    landmark = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username
    
    

