from django.shortcuts import render, redirect
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login, logout
# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request,user)
        return redirect('/')
    return render(request,'accounts/form.html', {'form': form, 'title': 'Login'})

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        user.set_password(password)
        #user.is_staff = True #admin paneline giriş yetkisi
        #user.is_superuser = True #kullanıcıya tam yetki verir
        user.save()
        new_user = authenticate(username=user.username, password= password)
        login(request,new_user)
        return redirect('/')
    return render(request, 'accounts/form.html', {'form': form, 'title': 'Register'})


def logout_view(request):
    logout(request)
    return redirect('/')