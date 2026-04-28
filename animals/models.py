from django.db import models
from django.urls import reverse

class Animal (models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(help_text="Age in years")
    weight = models.IntegerField(help_text="Weight in kilograms")
    born_in_captivity = models.BooleanField(default=False)
    date_added = models.DateField()

class Meta:
    ordering = ['name']

def __str__(self):
    return f"{self.name} (age {self.age})"

def get_absolute_url(self):
    return reverse('animals:animal-detail', kwargs={'pk': self.pk})