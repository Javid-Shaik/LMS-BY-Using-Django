from django.shortcuts import render , redirect
# Create your views here.
from my_app.models import RegisterModel , Books , Member , Borrowings
from django import forms
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os 
import re
import uuid
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

def register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        role = request.POST.get('role')
        # email valid
        if is_valid_email(email):
            
            if role=='admin':
                messages.error(request, "You are not allowed to be an admin...." , 'signup')
                return redirect('signup:register')
            
            
            if RegisterModel.objects.filter(username=username).exists():
                messages.error(request ,  "Username is already taken",'signup')
                return redirect("signup:register")        
            
            user = RegisterModel(
                    first_name = fname,
                    last_name = lname,
                    username = username,
                    email = email,
                    password = password,
                    profile_image = image,
                    phone = phone,
                    role = role,
                    address = address
                )
            if image:
                user.profile_image = image
            else:
                default_image_path = os.path.join(settings.MEDIA_ROOT, 'profile', 'default_user.jpg')
                
                # Check if the default image exists
                if default_storage.exists(default_image_path):
                    # Open the default image file
                    with default_storage.open(default_image_path, 'rb') as f:
                        # Create a ContentFile from the default image data
                        default_image = ContentFile(f.read(), name='default_user.jpg')
                        user.profile_image = default_image
            user.save()
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_url = f'http://{get_current_site(request)}/confirm/{uidb64}/{token}/'

            # Send the confirmation email
            render(request , "forms/email_confirmation.html"  , {
                'confirm_url':confirm_url
            })
            subject = 'Confirm Your Email'
            message = f"Dear {user.first_name} {user.last_name},\nPlease click the below link to verify your email.\n{confirm_url}"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "Registration successful! Please check your email for the confirmation link.")
            return redirect('signup:login_user')
        else :
            user.delete()
            messages.error(request , "Enter valid email address")
            redirect("signup:register") 
    
    return render(request,"forms/register.html")

def details(request):
    users = RegisterModel.objects.all()
    books = Books.objects.all()
    # if request.session['users']:
    #     pass
    print(users)
    return render(request,"forms/details.html",{
        "users":users , 'books':books
    })
    
def homepage(request):
    user = request.user
    if request.method == 'POST':
        return redirect('signup:register')
    return render(request , "forms/homepage.html" ,{
        'user':user
    } )

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request , username=username, password=password)
        print(user)
        if user is not None :
            login(request, user)
            return redirect('signup:homepage')
        
        else :
            messages.success(request, "Incorrect Email or Password..")
            return redirect('signup:login_user')
    else :
        return render(request, 'forms/login.html')

  
def logout_user(request):
    logout(request)
    messages.error(request, "You Were Logged Out...",'base')
    return redirect('signup:homepage')
    
def show_books(request):
    books = Books.objects.all() #filter(availability='Yes')
    return render(request , 'forms/show_books.html' , {
        'books' : books
    })
    
def featured_books(request):
    books = Books.objects.filter(availability="No")
    return render(request , 'forms/featured_books.html' , {
        'featured_books' : books
    })
    
def about_libraquest(request):
    return render(request , 'about_libraquest.html')


# email validation 


def is_valid_email(email):
    # Regular expression pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# def send_confirmation_email(user):
#     confirmation_link = reverse('confirm_email', args=[user.confirmation_token])
#     subject = 'Confirm Your Email'
#     message = f'Click the following link to confirm your email: {settings.BASE_URL}{confirmation_link}'
#     send_mail(subject, message, settings.EMAIL_FROM, [user.email])


def confirm_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = RegisterModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, RegisterModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Mark the email as confirmed (You need to add an email_confirmed field in your user model)
        user.email_confirmed = True
        user.save()
        messages.success(request, 'Your email has been confirmed! You can now login.')
    else:
        messages.error(request, 'The confirmation link is invalid or has expired.')

    return redirect('signup:login_user')

