from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'mainpage.html')

def validate_email(email): # -> bool
    pass

def hash_password(pw): # -> str
    pass

def validate_firstname(name): # -> bool
    pass

def validate_pricelimit(price): # -> bool
    pass

def validate_transactionname(name): # -> bool
    pass

def validate_category(name): # -> bool
    pass