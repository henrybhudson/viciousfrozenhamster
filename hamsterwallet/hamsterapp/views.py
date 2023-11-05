from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from hamsterapp.models import *
import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from hamsterapp.models import *
import datetime
import hashlib
import json
import os
from dotenv import load_dotenv
import openai

def hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

print(hash('demodurhack'))

category_set = {'Bills','Charity','Eating Out','Entertainment',
                      'Finances','Gegneral','Groceries','Holidays',
                      'Personal Care','Shopping','Transfers','Transport'
}

load_dotenv();
openai.api_key = os.getenv('API_KEY');

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
        # email = request.POST["email"]
        # pw = request.POST["password"]
        c = get_transactions(request)
        c["email"] = request.POST["email"]
        obj = users.objects.get(email=request.POST["email"]);
        c["priceLimit"] = obj.priceLimit;
        return render(request, 'home.html', c)
    except:
        return HttpResponseRedirect(reverse(''))

#Processing page requests
def process_login_request(request):
    try:
        email = request.POST["email"]
        pw = request.POST["password"]
        check_login(email, pw)
        return home_page(request)
    except:
        return HttpResponseRedirect(reverse('login'))
    
def process_register_request(request):
    try:
        email = request.POST["email"]
        pw = request.POST["password"]
        name = request.POST["name"]
        budget = 100
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

    if len(users.objects.filter(email=email)) != 0:
        raise Exception

    if float(price) < 0:
        raise Exception

    obj = users(email=email,password=hash(pw), firstName=name, priceLimit=100)
    obj.save()

# def change_category_price(category, email, price):
#     validate_category(category)
#     validate_price(price)
#     price_sum = users.objects.get(email=email).priceLimit
#     for c,_,p in categories.objects.filter(email=email):
#         if c != category:
#             price_sum -= p

#     if price_sum - price < 0 or price < 0:
#         raise Exception
    
#     obj = categories.objects.get(category=category, email=email)
#     obj.priceLimit = price
#     obj.save()

# def update_details(email, password, firstname, price):
#     obj = users.objects.get(email=email)
#     check_max_price(email, price)
#     validate_text(firstname,)
#     obj.priceLimit = price
#     obj.password = password
#     obj.firstName = firstname
#     obj.save()

def create_transaction(email, transaction_name, price):
    validate_text(transaction_name,TRANSACTION_LENGTH)
    # validate_price(price)
    # validate_category(category)
    
    
    chat_completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": f"Categorise the payment described '{transaction_name}' using one of the following categories. Just say the word.\nBills\nCharity\nFood\nEntertainment\nFinances\nGeneral\nGroceries\nHolidays\nPersonal Care\nShopping\nBank Transfers\nTransport"}]).choices[0].message.content;
    category = chat_completion.replace('.', '');

    time = datetime.datetime.today().strftime("%d %B %Y")
    price = str("{:.2f}".format(float(price)))
    obj = transactions(email_id=email, transactionName=transaction_name, price=price, category=category, date=time)
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
        
def category_entries(email, category):
    return [i.values() for i in transactions.objects.filter(email=email,category=category)]

#JSON requests
def add_transaction(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        itemName = data.get('description', 'N/A')
        price = data.get('price', 'N/A')
        email = data.get('email', 'N/A')

        create_transaction(email, itemName, price)
        return JsonResponse({})
    except:
        return HttpResponse(status=400)
    
def del_transaction(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', 'N/A')
        
        remove_transaction(id)
        return JsonResponse({})
    except:
        return HttpResponse(status=400)
    

def get_transactions(request):
    try:
        email = request.POST["email"]
        data = {}
        ts = []
        for t in transactions.objects.filter(email=email).values():
            ts.append(t)
        data["transactions"] = ts
        return data
    except:
        data = {}
        return data
    
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
    
def update_budget(request):
    try:
        data = json.loads(request.body.decode('utf-8'));
        budget = data.get('budget', 'N/A');
        email = data.get('email', 'N/A');
        
        obj = users.objects.get(email=email)
        obj.priceLimit = budget;
        obj.save();
        return JsonResponse({}) 
    except:
        return HttpResponse(status=400)

def meow():
    cat_sounds = ["meow", "purr", "hiss", "yowl", "growl"]
    print(random.choice(cat_sounds))

#def bark():
    dog_sounds = ["woof", "bark", "growl", "howl", "whimper"]
    print(random.choice(dog_sounds))

