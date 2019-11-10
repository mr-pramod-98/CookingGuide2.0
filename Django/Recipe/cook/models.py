from django.db import models


# Create your models here.
class RecipesDjango(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    directions = models.TextField()
