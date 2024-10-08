from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, logout, authenticate 



def signupaccount(request):
    return render(request, 'signupaccount.html',
                  {'form':UserCreationForm})

def logoutaccount(request): 
    logout(request) 
    return redirect('home') 


def loginaccount(request): 
    if request.method == 'GET': 
        return render(request, 'loginaccount.html', 
            {'form':AuthenticationForm}) 
    else: 
         user = authenticate(request, username=request.POST['username'], 
                            password=request.POST['password']) 
    if user is None: 
        return render(request,'loginaccount.html', 
                {'form': AuthenticationForm(), 
                'error': 'username and password do not match'}) 
    else: 
        login(request,user) 
        return redirect('home') 