from django.db import models

# Create your models here.

class Date(models.Model):
    date = models.DateField()

class Country(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)

class Exchange(models.Model):
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    date = models.ForeignKey(Date,on_delete=models.CASCADE)
    buy = models.FloatField()
    sell = models.FloatField()