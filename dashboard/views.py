from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login

# Create your views here.


def register_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user = User.objects.create_user(
            username, email, password, first_name=first_name, last_name=last_name)
    except IntegrityError:
        context = {'message': "Username taken"}
        return render(request, 'registration.html', context)

    context = {"message": "User created successfully"}
    user = authenticate(username=username, password=password)

    return render(request, 'dashboard.html', context)


def login_user(request):
    uname = request.POST['username']
    pswd = request.POST['password']
    user = authenticate(username=uname, password=pswd)
    print(request.POST)
    if user is not None:
        login(request, user)
        return render(request, 'dashboard.html')

    else:
        context = {'object': 'Login error try again'}
        return render(request, 'login.html', context)
