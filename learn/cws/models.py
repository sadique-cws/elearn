from django.db import models
from django.conf import settings
# Create your models here.
class Category(models.Model):
    cat_title = models.CharField(max_length=200)
    cat_slug = models.SlugField()
    cat_description = models.TextField()

    def __str__(self):
        return self.cat_title
    
class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.CharField(max_length=200)
    duration = models.DateTimeField()
    types = models.CharField(max_length=20)
    status = models.BooleanField()
    price = models.FloatField()
    course_slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered = models.BooleanField()
    items = models.ForeignKey(Course,on_delete=models.CASCADE)
    doc = models.DateTimeField(auto_now_add=True) 


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=15)
    ordered = models.BooleanField()
    items = models.ManyToManyField(OrderItem)
    starting_date = models.DateTimeField()
    ordered_date = models.DateTimeField()
    status = models.BooleanField()






