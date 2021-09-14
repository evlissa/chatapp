# chat/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout

from chat.forms import LoginForm, RegistrationForm

# ввод названия чат-комнаты
def enteringroom_view(request):
    if request.user.is_authenticated:
        return render(request, 'chat/enteringroom.html', {})
    else:
        return redirect('login')

# страница аутентификации пользователя
def login_view(request, *args, **kwargs):
    
    context = {}

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username = username, password = password)
            if user:
                login(request, user)
                return redirect('enter')
        else:
            context['login_form'] = form

    return render(request, 'chat/login.html', context)

# выход из аккаунта
def logout_view(request):
    logout(request)
    return redirect("login")

# регистрация пользователя
def register_view(request, *args, **kwargs):

    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as {user.username}.")
    context = {}
    
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username = username, password=raw_password)
            login(request, account)
            return redirect("enter")
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'chat/register.html', context)

# чат-комната
def room(request, room_name):
    if request.user.is_authenticated:
        return render(request, 'chat/room.html', {
            'room_name': room_name, 
        })
    else:
        return redirect('login')
