from django.db import models

# Create your models here.
class Category(models.Model):
    cat_title = models.CharField(max_length=200)
    cat_slug = models.SlugField()
    cat_description = models.TextField()

    def __str__(self):
        return self.cat_title
    