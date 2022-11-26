from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=70)
    
    def __str__(self) -> str:
        return self.name

    

class Recipe(models.Model):
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=170)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=70)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=70)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d', blank=True, default='')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,
                                blank=True, default=None)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    
    def __str__(self) -> str:
        return self.title
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}'
            
        super().save(*args, **kwargs)