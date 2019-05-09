from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth import get_user_model

# Create your views here.

def login(request):
    request_method = request.method
    print('request_method = ' + request_method)
    if request_method == 'POST':
        user_name = request.POST.get('user_name', '')
        user_password = request.POST.get('user_password', '')
        # authenticate user account.
        user = auth.authenticate(request, username=user_name, password=user_password)
        if user is not None:
            # login user account.
            auth.login(request, user)
            response = HttpResponseRedirect('/user/login_success/')
            # set cookie to transfer user name to login success page.
            response.set_cookie('user_name', user_name, 3600)
            return response
        else:
            error_json = {'error_message': 'User name or password is not correct.'}
            return render(request, 'users/login.html', error_json)
    else:
        return render(request, 'users/login.html')

def register(request):
    #if request.method == 'POST':
    #    form = UserCreationForm(data=request.POST)
    #    if form.is_valid():
    #        form.save()
    #        return redirect("login")
    #return render(request, "users/register.html", {
    #    'form': UserCreationForm()
    #})

    request_method = request.method
    print('request_method = ' + request_method)
    if request_method == 'POST':
        print('test', request.POST)
        user_name = request.POST.get('user_name', '')
        user_password = request.POST.get('user_password', '')
        user_email = request.POST.get('email', '')
        if len(user_name) > 0 and len(user_password) > 0 and len(user_email) > 0:
            # check whether user account exist or not.
            user = auth.authenticate(request, username=user_name, password=user_password)
            # if user account do not exist.
            if user is None:
                # create user account and return the user object.
                user = get_user_model().objects.create_user(username=user_name, password=user_password,
                                                            email=user_email)
                # update user object staff field value and save to db.
                if user is not None:
                    user.is_staff = True
                    # save user properties in sqlite auth_user table.
                    user.save()
                # redirect web page to register success page.
                response = HttpResponseRedirect('/user/register_success/')
                # set user name, password and email value in session.
                request.session['user_name'] = user_name
                request.session['user_password'] = user_password
                request.session['user_email'] = user_email
                return response
                print("USER CREATED!!!")
            else:
                error_json = {'error_message': 'User account exist, please register another one.'}
                return render(request, 'users/register.html', error_json)
        else:
            error_json = {'error_message': 'User name, password and email can not be empty.'}
            return render(request, 'users/register.html', error_json)
    else:
        return render(request, 'users/register.html')

def forgot_pass(request):
    return render(request, "users/forgot_pass.html")

def register_success(request):
    return render(request, "user/register_success")