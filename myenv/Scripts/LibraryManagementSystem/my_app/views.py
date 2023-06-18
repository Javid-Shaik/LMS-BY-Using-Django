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
        print(role)
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
        return redirect('signup:login_user')
    return render(request,"forms/register.html")

def details(request):
    users = RegisterModel.objects.all()
    # if request.session['users']:
    #     pass
    print(users)
    return render(request,"forms/details.html",{
        "users":users
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
