from django.db import models

# Create your models here.
class users(models.Model):
    email = models.CharField(max_length=32,primary_key=True)
    password = models.CharField(max_length=255)
    firstName = models.CharField(max_length=32)
    priceLimit = models.IntegerField()

class categories(models.Model):
    category = models.CharField(max_length=64)
    priceLimit = models.IntegerField()

class transactions(models.Model):
    transactionID = models.IntegerField(primary_key=True)
    email = models.ForeignKey(users, on_delete=models.CASCADE)
    transactionName = models.CharField(max_length=255)
    price = models.IntegerField()
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    date = models.DateTimeField()
