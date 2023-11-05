from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from hamsterapp.models import *
import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from hamsterapp.models import *
import datetime
import hashlib

def hash():
    return hashlib.sha256(str.encode())


category_set = {'Bills','Charity','Eating Out','Entertainment',
                      'Finances','Gegneral','Groceries','Holidays',
                      'Personal Care','Shopping','Transfers','Transport'
}


#Site pages
def login_page(request):
    return render(request,'login.html')
def register_page(request):
    try:
        email = request.POST["email"]
        return HttpResponseRedirect(reverse(''))
    except:
        return render(request, 'register.html')
def home_page(request):
    try:
        email = request.POST["email"]
        pw = request.POST["password"]
        return render(request, 'home.html')
    except:
        return HttpResponseRedirect(reverse(''))

#Processing page requests
def process_login_request(request):
    try:
        email = request.POST["email"]
        pw = request.POST["password"]
        check_login(email,pw)
        return home_page(request)
    except:
        return HttpResponseRedirect(reverse('login'))
def process_register_request(request):
    try:
        email = request.POST["email"]
        pw = request.POST["password"]
        name = request.POST["name"]
        budget = float(request.POST["budget"])
        register(email,pw,name,budget)
        return home_page(request)
    except:
        return HttpResponseRedirect(reverse('registersite'))

#Validation functions
def validate_email(email): # -> bool
    if '@' not in email:
        raise Exception
def validate_text(text, size):
    if type(text)!=str:
        raise Exception
    if not (1 <= len(text) <= size):
        raise Exception
def validate_price(price):
    if type(price)!=float:
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
    if obj.password != hash(pw):
        raise Exception

#Database functions
def register(email, pw, name, price):
    validate_email(email)
    validate_price(price)
    validate_text(pw, PASSWORD_LENGTH)
    validate_text(name, FIRSTNAME_LENGTH)


    if len(users.objects.filter(email=email)) != 0:
        raise Exception

    if price < 0:
        raise Exception

    obj = users(email=email,password=hash(pw), firstName=name, priceLimit=price)
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

# def update_details(email, password, firstname, price):
#     obj = users.objects.get(email=email)
#     check_max_price(email, price)
#     validate_text(firstname,)
#     obj.priceLimit = price
#     obj.password = password
#     obj.firstName = firstname
#     obj.save()

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

#Database observations
def sum_category(email, category):
    validate_category(category)
    s = 0
    for i in transactions.objects.filter(email=email,category=category):
        s += i.price
    return [s,categories.objects.get(email=email,category=category).priceLimit]
def category_entries(email, category):
    return [i.values() for i in transactions.objects.filter(email=email,category=category)]

#JSON requests
def add_transaction(request):
    try:
        email = request.POST["email"]
        itemName = request.POST["name"]
        price = float(request.POST["price"])
        category = request.POST["category"]
        add_transaction(email, itemName, price, category)
    except:
        pass

def get_transactions(request):
    try:
        email = request.POST["email"]
        data = {}
        for a,b,c,d,e,f in transactions.objects.filter(email=email).values():
            data[a] = [b,c,d,e,f]
        return JsonResponse(data)
    except:
        data = {}
        return JsonResponse(data)
    
def get_category_sum(request):
    try:
        email = request.POST["email"]
        category = request.POST["category"]
        a,b = sum_category(email,category)
        data = {}
        data[a] = b
        return JsonResponse(data)

    except:
        return JsonResponse({})
    

# ...

def get_transactions(request):
    try:
        email = request.session['email']
        data = {}
        for a,b,c,d,e,f in transactions.objects.filter(email=email).values():
            data[a] = [b,c,d,e,f]
        return JsonResponse(data)
    except:
        data = {}
        return JsonResponse(data)
