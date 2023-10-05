from django.db.models import Count
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login ,authenticate,update_session_auth_hash
from django.contrib.auth import authenticate, login as auth_login
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from .manager import UserManager
from django.shortcuts import render, get_object_or_404
from django.contrib  import messages,auth
from .models import CustomUser,UserProfile
from FindMyNestApp.models import Subscription
from Customer.models import Property
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
import requests
from social_django.utils import psa
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()


def login(request):
    # Check if the user is already authenticated
    if request.user.is_authenticated:
        if request.user.user_type == CustomUser.ADMIN:
            return redirect(reverse('admindashboard'))
        elif request.user.user_type == CustomUser.CUSTOMER:
            return redirect(reverse('index'))
        else:
            return redirect('/')
    
    if request.method == 'POST':
        # captcha_token = request.POST.get("g-recaptcha-response")
        # cap_url = "https://www.google.com/recaptcha/api/siteverify"
        # cap_secret = "6LcJj44nAAAAADDjTqz0n5e7UM5HRFzMtC54swC3"
        # cap_data = {"secret": cap_secret, "response": captcha_token}
        
        # cap_server_response = requests.post(url=cap_url, data=cap_data)
        # cap_json = json.loads(cap_server_response.text)
        
        # if not cap_json['success']:
        #     return HttpResponseRedirect(reverse('login') + '?alert=invalid_captcha') 

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)

                if request.user.user_type == CustomUser.ADMIN:
                    return redirect(reverse('admindashboard'))
                elif request.user.user_type == CustomUser.CUSTOMER:
                    return redirect(reverse('index'))
                else:
                    return redirect('/')
            else:
                return HttpResponseRedirect(reverse('login') + '?alert=invalid_credentials')
        else:
            return HttpResponseRedirect(reverse('login') + '?alert=fill_fields')

    return render(request, 'accounts/google/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        cpassword = request.POST.get('confirmPassword', None)

        if username and first_name and last_name and email and phone and password:

            if User.objects.filter(username=username).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=username_is_already_registered')

            elif User.objects.filter(email=email).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=email_is_already_registered')

            elif User.objects.filter(phone_no=phone).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=phone_no_is_already_registered')
            
            elif password != cpassword: 
                return HttpResponseRedirect(reverse('register') + '?alert=passwords_do_not_match')
                

            else:
                user = User(username=username, first_name=first_name, last_name=last_name, email=email, phone_no=phone)
                user.set_password(password)  # Set the password securely
                user.save()

                user_profile = UserProfile(user=user)
                user_profile.save()
                return HttpResponseRedirect(reverse('login') + '?alert=registered')

    return render(request, 'register.html')

      
def reset_password(request):
    return redirect('reset_password.html')

@login_required
def admindashboard(request):
    user_count = User.objects.exclude(is_superuser=True).count()
    property_count = Property.objects.count()
    properties = Property.objects.all()
    users = User.objects.exclude(is_superuser=True)
    subscription_count = Subscription.objects.count()
    property_type_counts = Property.objects.values('property_type').annotate(count=Count('property_type')).order_by('property_type')
    
    
    context = {
        'user_count': user_count,
        'property_count': property_count,
        'property_type_counts': property_type_counts,
        'users': users,
        'properties': properties,
        'subscription_count': subscription_count,
    }
    
    return render(request, 'Admin-DashBoard.html', context)


def users(request):
    user_count = User.objects.exclude(is_superuser=True).count()
    users = User.objects.exclude(is_superuser=True)
    
    context = {
        'user_count': user_count,
        'users': users,
    }
    
    return render(request, 'users_list.html', context)

def propertys(request):
    properties = Property.objects.all()

    
    context = {
        'properties': properties,
    }
    
    return render(request, 'Property_list.html', context)

def subscription(request):
    subscriptions = Subscription.objects.all()

    
    context = {
        'subscriptions': subscriptions,
    }
    
    return render(request, 'Subscription.html', context)

 
def editprofile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_properties = Property.objects.filter(user=request.user)

    if request.method == 'POST':
        # Get the phone number entered by the user
        new_phone_no = request.POST.get('phone_no')

        # Check if the phone number already exists for a different user
        existing_user = UserProfile.objects.filter(user__phone_no=new_phone_no).exclude(user=request.user).first()
        if existing_user:
            error_message = "Phone number is already registered by another user."
            return HttpResponseRedirect(reverse('editprofile') + f'?alert={error_message}')
        
        if new_phone_no:
            user.phone_no = new_phone_no
            user.save()

        # Update user fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        new_profile_pic = request.FILES.get('profile_pic')
        if new_profile_pic:
            user_profile.profile_pic = new_profile_pic

        # Update user profile fields
        user_profile.country = request.POST.get('country')
        user_profile.state = request.POST.get('state')
        user_profile.city = request.POST.get('city')
        user_profile.pin_code = request.POST.get('pin_code')
        user_profile.save()

        return redirect('editprofile')

    context = {
        'user': user,
        'user_profile': user_profile,
        'user_properties': user_properties
    }

    return render(request, 'editprofile.html', context)



def googleProfileComplte(request):
    user = request.user

    if request.method == 'POST':
        new_phone_no = request.POST.get('phone_no')  # Correct variable name
        existing_user = User.objects.filter(phone_no=new_phone_no).exclude(pk=user.pk).first()

        if existing_user:
            error_message = "Phone number is already registered by another user."
            return HttpResponseRedirect(reverse('editprofile') + f'?alert={error_message}')

        if new_phone_no:
            user.phone_no = new_phone_no
            user.save()

        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile(user=user)

        user_profile.save()
        return redirect('index')

    context = {
        'user': user,
    }
    return render(request, 'profile_completion.html', context)

          





def logout(request):
     auth.logout(request)
     return redirect('/')


@login_required
def change_password(request):
    val = 0  
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    user_properties = Property.objects.filter(user=request.user)
    
    error_message = None  # Initialize error_message
    
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if user.check_password(current_password):
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                
                # Update the session with the new authentication hash
                update_session_auth_hash(request, user)

                # Redirect with success message
                return HttpResponseRedirect(reverse('editprofile') + '?alert=Password changed successfully.')
            else:
                # Set error message for password mismatch
                error_message = 'New password and confirm password do not match.'
        else:
            # Set error message for incorrect current password
            error_message = 'Incorrect current password.'
    
    context = {
        'user': user,
        'user_profile': user_profile,
        'user_properties': user_properties
    }

    # Redirect with error message (if any)
    if error_message:
        return HttpResponseRedirect(reverse('editprofile') + f'?alert={error_message}')
    
    return render(request, 'editprofile.html', context)

def view_all_users(request):
    users = CustomUser.objects.all()
    
    context = {
        'users': users,
    }
    
    return render(request, 'User_list.html', context)

def deleteUser(request, delete_id):
    delUser=User.objects.get(id=delete_id)
    delUser.delete()
    return redirect('users')

def delete_property(request, property_id):

    property_obj = get_object_or_404(Property, id=property_id)

    if request.user == property_obj.user:
        property_obj.active = False
        property_obj.save()
        
    return redirect('admindashboard')


def updateStatus(request,update_id):
    updateUser=User.objects.get(id=update_id)
    if updateUser.is_active==True:
        updateUser.is_active=False
    else:
        updateUser.is_active=True
    updateUser.save()
    return redirect('users')


def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user)
    
    # Count the number of properties posted by the user
    properties = Property.objects.filter(user=user).annotate(property_count=Count('user'))
    
    # Get the last posted property by the user
    last_posted_property = Property.objects.filter(user=user).order_by('-created_at').first()
    
    # Get the created and modified dates of the last posted property
    last_posted_property_created_at = last_posted_property.created_at if last_posted_property else None
    last_posted_property_modified_at = last_posted_property.modified_at if last_posted_property else None
    
    inactive_property_count = Property.objects.filter(user=user, active=False).count()
    
    superuser = User.objects.filter(is_superuser=True).first() 
    
    context = {
        'user': user,
        'user_profile': user_profile,
        'properties': properties,
        'superuser': superuser,
        'last_posted_property_created_at': last_posted_property_created_at,
        'last_posted_property_modified_at': last_posted_property_modified_at,
        'inactive_property_count': inactive_property_count,  # Include the count in the context
    }
    
    return render(request, 'user_details.html', context)


def updateuserStatus(request,update_id):
    updateUser=User.objects.get(id=update_id)
    if updateUser.is_active==True:
        updateUser.is_active=False
    else:
        updateUser.is_active=True
    updateUser.save()
    return redirect('user_details', user_id=update_id)

