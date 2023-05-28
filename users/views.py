from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password
from django.http import Http404, HttpResponse
from django.urls import reverse
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

import uuid
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash

from list.forms import LinkModelForm
from list.models import Link
from core.utils import generate_qr_code
from .forms import RegisterUserForm, UserModelForm, UserProfileModelForm
from .models import User
from .utils import paginate_users

# Create your views here.
class UsersRegisterUser(View):
    def get(self,request):
        form = RegisterUserForm()
        context = {
           'next': 'core:index',
           'form': form
        }
        #return render(request, 'signup.html', context)
        return render( request, 'registration/signup.html', context)


    def post(self, request):
        print(request.POST)
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print('Checking User...')
            username = form.cleaned_data['username']
            found = True
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                found = False    

            if found == True:
                messages.error(request,'Username already exists.')
                context = {
                    'next': 'core:index',
                    'form': form
                }
                    
                return render( request, 'registration/signup.html', context)

            password = form.cleaned_data['password1']
            password_hash = make_password(password)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user = User(username=username,password=password_hash,first_name=first_name,last_name=last_name,email=email,is_staff=False,is_active=False,is_superuser=False)
            user.save()
            user.send_activation()
            messages.success(request, "User activation email has been sent.")
        else:
            messages.error(request,'Error in form validation.')
            context = {
                'next': 'core:index',
                'form': form
            }
                
            return render( request, 'registration/signup.html', context)
        return redirect('core:index')
            
        
class UsersActivateUser(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id = uid)
        except:
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated.')
            return redirect('core:index')
        else:
            messages.error(request, 'Invalid activation link.')
            return redirect('core:index')

class UsersResetPassword(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id = uid)
        except:
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            context = {
               'user': user,
               'next': 'core:index',
               'uidb64': uidb64, 
               'token': token
            }
            return render(request, 'users/reset_password.html', context)
        else:
            messages.error(request, 'Invalid link.')
            return redirect('core:index')
        
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id = uid)
        except:
            messages.error(request, 'Error setting new password.')
            return redirect('users:reset_password', uidb64=request.POST['uidb64'], token=request.POST['token'])
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            if password != confirm_password:
                messages.error(request, 'Your passwords do not match.')
                return redirect('users:reset_password', uidb64=request.POST['uidb64'], token=request.POST['token'])
            password_hash = make_password(password)
            user.password = password_hash
            user.save()
            messages.success(request, 'Your password has been reset.')
            return redirect('core:index')
        else:
            messages.error(request, 'Error setting new password.')
            return redirect('users:reset_password', uidb64=request.POST['uidb64'], token=request.POST['token'])
class UsersForgotPassword(View):
    def get(self, request):
        context = {
            'next': 'core:index'
        }
        return render(request, 'users/forgot_password.html', context)
    def post(self, request):
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
          
            user.is_active = False
           
            user.save()           
            user.send_password_reset()
            
        except:
            pass

        messages.info(request, "An email has been sent.  If you don't receive the link, check your SPAM folder or verify the email address and try again.")    

        return redirect('core:index')

class UsersSearch(View):
    def get(self, request):
        print(request.GET)

        search_query = ''

        search_query = request.GET.get('search_query', '')

        links = Link.objects.filter(Q(type__icontains=search_query) | Q(link__icontains=search_query))
        users = User.objects.distinct().filter(Q(is_superuser=False)&(Q(username__icontains=search_query) | Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | 
                                                          Q(email__icontains=search_query) | Q(link__in=links) |
                                                          Q(user_profile__short_intro__icontains=search_query) |
                                                          Q(user_profile__bio__icontains=search_query))).defer('password')
        
        custom_range, users = paginate_users(request, users, 10)
        context = {
            'users': users,
            'custom_range': custom_range,
            'search_query': search_query
        }
        return render(request, 'users/search.html', context)
    
class UsersViewProfile(View):
    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
        except:
            messages.error(request, "Cannot load profile.")
            return redirect('core:index')
        links = []
        profile_link = f'http://{settings.APP_URL}/users/{user.id}'
        stream = generate_qr_code(profile_link)
        context = {
            'user': user,
            'links': links,
            'profile_link': profile_link,
            'qrcode': stream.getvalue().decode()
        }
        return render(request, 'users/profile.html', context)

class UsersViewShortIntro(View):
    def get(self, request, pk):
        if request.htmx == False:
            return Http404
        try:
            user = User.objects.get(id=pk)
        except:
            user = None
        context = {
            'user': user
        }
        return render(request, 'users/partials/short_intro.html', context)

class UsersEditShortIntro(LoginRequiredMixin, View):
    def get(self, request, pk):
        if request.htmx == False:
            return Http404
        try:
            user = User.objects.get(id=pk)
        except:
            user = None
        context = {
            'user': user
        }
        return render(request, 'users/partials/update_intro.html', context)
    def post(self, request, pk):
        if request.htmx == False:
            return Http404
        try:
            user = User.objects.get(id=pk)
        except:
            user = None
        if request.user.id == user.id:
            short_intro = request.POST['short_intro']
            user.user_profile.short_intro = short_intro
            user.user_profile.save()

        context = {
            'user': user
        }
        return render(request, 'users/partials/short_intro.html', context)

class DownloadQRCode(View):
    def get(self, request):
        
        url = request.GET.get('url')
            
        stream = generate_qr_code(url)

        headers = {
                'Content-Type': 'image/svg+xml',
                'Content-Disposition': 'inline; filename="qrcode.svg"'
            }
            
        return HttpResponse(stream.getvalue().decode(), headers=headers)

#@login_required(login_url='login')
def get_profile(request, pk):
    if request.htmx == False:
        return Http404
    try:
        user = User.objects.get(id= pk)
        links = list(Link.objects.filter(user=user).values('type','link'))
    except:
        messages.error(request, "Cannot load profile.")
        return redirect('core:index')
    for link in links:
        temp_link = Link(type=link['type'])
        link['label'] = temp_link.get_type_display()

    
    context = {
        'user': user,
        'links': links,
        'tab': 1
    }
    return render(request, 'users/partials/tab.html', context)

@login_required(login_url='login')
def edit_profile(request, pk):
    if request.htmx == False:
        return Http404
    try:
        user = User.objects.get(id= pk)
    except:
        messages.error(request, "Cannot load profile.")
        return redirect('core:index')
    if request.method == 'POST':
        user_form = UserModelForm(request.POST, instance=user)
        profile_form = UserProfileModelForm(request.POST, request.FILES, instance=user.user_profile)
        link_form = LinkModelForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid() and link_form.is_valid:
            print("saving data...")
            user_form.save()
            profile_form.save()
           
        context = {
        'user': user,
        'tab': 1
        }
        return render(request, 'users/partials/tab.html', context)
    user_form = UserModelForm(instance=user)
    profile_form = UserProfileModelForm(instance=user.user_profile)
   
    context = {
        'user': user,
        'tab': 2,
        'user_form': user_form,
        'profile_form': profile_form,
   
    }
    return render(request, 'users/partials/tab.html', context)

@login_required(login_url='login')
def change_password(request, pk):
    if request.htmx == False:
        return Http404
    
    try:
        user = User.objects.get(id= pk)
    except:
        messages.error(request, "Cannot load profile.")
        return render(request, 'users/partials/tab.html', {'user': None, 'tab': 99})
    context = {
        'user': user,
        'tab': 99
    }
    if request.method == "POST":
        print(request.POST)
        # check password with current password
        password = request.POST['password']
       
        try:
            print(user.password)
            password_match = check_password(password, user.password)
        except:
            messages.error(request, "Current password is incorrect.")
            return render(request, 'users/partials/tab.html', context)
        if password_match == False:
            messages.error(request, "Current password is incorrect.")
            return render(request, 'users/partials/tab.html', context)
        # check if new password matches confirm password
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return render(request, 'users/partials/tab.html', context)
        # check if the new password is valid before saving
        try:
            validate_password(new_password, user)
        except Exception as ex:
            for msg in ex.messages:
                messages.add_message(request, messages.ERROR, msg)
                return render(request, 'users/partials/tab.html', context)
        update_password = make_password(new_password)
        user.password = update_password
        user.save()
        messages.success(request, "Your password has been changed.")

        return render(request, 'users/partials/tab.html', context)
        

    
    return render(request, 'users/partials/tab.html', context)