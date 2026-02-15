from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from devices import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('devices.urls')),
    
    # Головна сторінка: тепер вона автоматично перенаправляє на твій API
    path('', RedirectView.as_view(url='/api/devices/', permanent=True)),
    
    # Шляхи для Лабораторної №6 (Автентифікація)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_with_2fa_view, name='login'),
    path('verify-2fa/', views.verify_2fa_view, name='verify_2fa'),
    path('secure/', views.secure_page, name='secure'), 
    
    # Вихід із системи
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]