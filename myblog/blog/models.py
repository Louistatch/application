from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from django.template.defaultfilters import striptags

class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    desc = HTMLField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    duration_in_hours = models.PositiveIntegerField(default=0)
    instructor = models.CharField(max_length=100, default='Instructeur par défaut')
    prerequisites = models.TextField(blank=True)
    materials = models.TextField(blank=True)
    certification = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("my-articles")

    def get_desc_without_html(self):
        return striptags(self.desc)
