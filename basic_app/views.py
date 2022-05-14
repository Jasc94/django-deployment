from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

def register(request):
    # We assume at first that the user is not registered
    registered = False
    if request.method == 'POST':
        # We grab the info from the form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # We check if the info in the form was valid and then write in the database
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # We don't want to save it to the db yet
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    # If it isn't a POST request, then we just set the form to be filled
    else:
        user_form =  UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
                  {'user_form':user_form,
                   'profile_form':profile_form,
                   'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authentication
        user = authenticate(username=username, password=password)

        if user:
            # if the user is active (has an account)
            if user.is_active:
                login(request, user)
                # If the login is succesful, the user will be redirected to the homepage
                return HttpResponseRedirect(reverse('index'))
            
            # if the account is not active
            else:
                return HttpResponse('ACCOUNT IS NOT ACTIVE')
        else:
            print('Someone tried to login and failed!')
            print(f"Username: {username} and password {password}")
            return HttpResponse('Invalid login details supplied!')
    # In case the user hasn't sent any form (so, basically any other status)
    else:
        return render(request, 'basic_app/login.html', {})

# The decorator checks whether the user is logged in
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse('You are logged in. Nice!')