from django.shortcuts import render , redirect , get_object_or_404
from my_app.models import UserManager , RegisterModel , Member , Books , Borrowings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
# from django.contrib import messages
from datetime import date, timedelta
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.
def user_profile(request , username ):
    try :
        member = Member.objects.get(user__username=username)
    except Member.DoesNotExist:
        # If Member object doesn't exist, create a new one
        user = RegisterModel.objects.get(username=username)
        member = Member.objects.create(user=user, address=user.address ,phone=user.phone)
    borrowings = member.borrowings_set.all()
    
    return render(request, 'profile/user_profile.html', {
        'user': request.user , 'borrowings' : borrowings
    })
    
def edit_profile(request):
    return render(request, 'profile/edit_profile.html',{
        'user':request.user
    })

def save_profile(request , username):
    username = request.user.username
    profile = get_object_or_404(RegisterModel, username=username)
    if request.method == 'POST':
        
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        if fname :
            profile.first_name = fname
        if lname :
            profile.last_name = lname
        if address :
            profile.address = address  
        if image :
            profile.profile_image = image
        
        profile.email = email
        profile.phone = phone
        profile.save()
        
        return redirect('user_profile' , username=username)
    
    return render(request , 'profile/edit_profile.html')

def borrow_books(request , book_id):
    book = Books.objects.get(id=book_id)
    print(book)
    member = Member.objects.get(user=request.user)
    borrowed_date = date.today()
    due_date = borrowed_date + timedelta(days=14)
    
    if book.availability == 'No':
        message = f"The book {book.title} is currently not available."
        return JsonResponse({'message': message, 'success': False})
    else:
        message = f"You have successfully borrowed {book.title}"
        borrowing = Borrowings(
            book=book,
            member=member,
            borrowed_date=borrowed_date,
            due_date=due_date,
            status='Borrowed'
        )
        borrowing.save()
        book.availability = 'No'
        book.save()
        return JsonResponse({'message': message, 'success': True})
    
def book_search(request):
    book_domain = request.GET.get('book_domain')
    search_text = request.GET.get('text')
    books = None
    lookup = Q()
    if book_domain == 'All':
        lookup = Q(title__icontains=search_text) | Q(author_name__icontains=search_text) | Q(isbn__icontains=search_text)
    if book_domain == 'Title':
        lookup |= Q(title__icontains=search_text)
    elif book_domain == 'Author':
        lookup |= Q(author_name__icontains=search_text)
    elif book_domain == 'Isbn':
        lookup |= Q(isbn__icontains=search_text)
    books = Books.objects.filter(lookup)
    return render(request , 'books/book_search.html', {
        'books' : books,
        # 'query' : lookup
    })
    
    
