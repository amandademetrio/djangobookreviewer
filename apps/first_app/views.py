from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import *
from django.contrib import messages

def index(request): #Renders initial screen with registration and login options
    return render(request,'first_app/index.html')

def sucess(request): #Renders the page with the sucess message, after registration process or login
    return render(request,'first_app/success.html')

def registration(request): #Handles registration process and sets up session with information
    errors = User.objects.basic_validator(request.POST)

    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='registration_errors')
        return redirect('/')
    
    else:
        new_user = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        new_user.save()
        request.session['first_name'] = new_user.first_name
        request.session['last_name'] = new_user.last_name
        request.session['email'] = new_user.email
        request.session['logged_in'] = True
        request.session['user_id'] = new_user.id
        return redirect('/sucess')

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    errors = User.objects.login_validator(request.POST)
    
    if len(errors):
        for key,value in errors.items():
            messages.error(request,value,extra_tags='login_errors')
        return redirect('/')
    
    else:
        login_user = User.objects.get(email=request.POST['email'])
        request.session['logged_in'] = True
        request.session['user_id'] = login_user.id
        return redirect('/sucess')