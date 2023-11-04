from django.shortcuts import render
from hamsterapp.models import *
import datetime
import re

category_set = set('Bills','Charity','Eating Out','Entertainment',
                      'Finances','Gegneral','Groceries','Holidays',
                      'Personal Care','Shopping','Transfers','Transport'
                      )

def index(request):
    return render(request,'mainpage.html')

def validate_email(email): # -> bool
    email_pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$)'
    return re.match(email_pattern, email) is not None

def validate_text(text, size):
    if type(text)!=str:
        raise Exception
    if not (1 <= len(text) <= size):
        raise Exception

def validate_price(price):
    if type(price)!=int:
        raise Exception

def validate_category(name): # -> bool
    if type(name) != str:
        raise Exception
    if name not in category_set:
        raise Exception

def check_max_price(email, price):
    validate_email(email)
    validate_price(price)
        
    price_sum = 0
    for _,_,p in categories.objects.filter(email=email):
        price_sum += p

    if price < price_sum or price < 0:
        raise Exception

def check_login(email, pw):
    validate_text(pw,PASSWORD_LENGTH)
    obj = users.objects.get(email=email)
    return obj.password == pw



def register(email, pw, name, price):
    validate_email(email)
    validate_price(price)
    validate_text(pw, PASSWORD_LENGTH)
    validate_text(name, FIRSTNAME_LENGTH)
    
    for em,_,_ in users.objects.all().values():
        if em == email:
            raise Exception

    if price < 0:
        raise Exception

    obj = users(email=email,password=pw, price=price)
    obj.save()

def change_category_price(category, email, price):
    validate_category(category)
    validate_price(price)
    price_sum = users.objects.get(email=email).priceLimit
    for c,_,p in categories.objects.filter(email=email):
        if c != category:
            price_sum -= p

    if price_sum - price < 0 or price < 0:
        raise Exception
    
    obj = categories.objects.get(category=category, email=email)
    obj.priceLimit = price
    obj.save()

def update_details(email, password, firstname, price):
    obj = users.objects.get(email=email)
    check_max_price(email, price)
    validate_text(firstname,)
    obj.priceLimit = price
    obj.password = password
    obj.firstName = firstname
    obj.save()

def add_transaction(email, transaction_name, price, category):
    validate_text(transaction_name,TRANSACTION_LENGTH)
    validate_price(price)
    validate_category(category)

    time = datetime.datetime.now().astimezone()
    obj = transactions(email, transaction_name, price, category, time)
    obj.save()
    
def remove_transaction(transaction_ID):
    obj = transactions.objects.get(id=transaction_ID)
    obj.delete()
