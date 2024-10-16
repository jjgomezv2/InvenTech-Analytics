from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserProfileForm

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Managers').exists())
def signupaccount(request):
    if request.method == 'GET':
        user_form = UserCreationForm()
        profile_form = UserProfileForm()
        return render(request, 'signupaccount.html',
                  {'user_form': user_form, 'profile_form': profile_form})
    else:

        user_form = UserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            if request.POST['password1'] == request.POST['password2']:
                user = user_form.save()
                
                profile = profile_form.save(commit=False)
                profile.user = user
                profile.company_idCompany = request.user.userprofile.company_idCompany
                profile.save()
                
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'signupaccount.html', 
                              {'user_form': user_form, 'profile_form': profile_form, 'error': 'Passwords do not match'})
        else:
            return render(request, 'signupaccount.html', 
                              {'user_form': user_form, 'profile_form': profile_form, 'error': 'Form Validation Error'})

@login_required
def logoutaccount(request): 
    logout(request) 
    return redirect('landing') 


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
    
def landing(request):
    return render(request, 'landing.html')