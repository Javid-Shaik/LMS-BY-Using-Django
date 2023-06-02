from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'signup'
urlpatterns = [
    path("login", views.login_user , name="login_user"),
    path("register" , views.register , name = "register"),
    path("details", views.details , name="details"),
    path("",views.homepage, name="homepage"),
    path("logout_user",views.logout_user, name="logout"),
    path('show_books', views.show_books , name='show_books'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
