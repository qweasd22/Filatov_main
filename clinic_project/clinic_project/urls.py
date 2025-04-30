from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from clinic import views
from users import views as user_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinic.urls')),
    path('register/', user_views.register, name='register'),
    path('',include('users.urls')),
    path('',include('billing.urls')),
    path('login/', LoginView.as_view(template_name='registration/login.html',next_page='home'), name='login'),
    
]