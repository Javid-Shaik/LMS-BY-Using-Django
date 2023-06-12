from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/<str:username>/', views.user_profile , name='user_profile'),
    path('edit_profile/' , views.edit_profile , name='edit_profile'),
    path('save_profile/<str:username>/',views.save_profile , name='save_profile'),
    path('borrow_books/<int:book_id>/' , views.borrow_books, name='borrow_books'),
    path('book_search/' , views.book_search , name='book_search')
]