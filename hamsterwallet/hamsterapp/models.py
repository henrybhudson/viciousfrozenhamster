from django.db import models

FIRSTNAME_LENGTH = 64
PASSWORD_LENGTH = 255
EMAIL_LENGTH = 32
TRANSACTION_LENGTH = 255
CATEGORY_LENGTH = 64

# Create your models here.
class users(models.Model):
    email = models.CharField(max_length=EMAIL_LENGTH,primary_key=True)
    password = models.CharField(max_length=PASSWORD_LENGTH)
    firstName = models.CharField(max_length=FIRSTNAME_LENGTH)
    priceLimit = models.IntegerField()

class categories(models.Model):
    category = models.CharField(max_length=CATEGORY_LENGTH,primary_key=True)
    email = models.ForeignKey(users, on_delete=models.CASCADE)
    priceLimit = models.IntegerField()

class transactions(models.Model):
    email = models.ForeignKey(users, on_delete=models.CASCADE)
    transactionName = models.CharField(max_length=TRANSACTION_LENGTH)
    price = models.IntegerField()
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    date = models.DateTimeField()

