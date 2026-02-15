from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from devices import views # Импортируем твои новые функции из views.py

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('devices.urls')),
    path('', RedirectView.as_view(url='/api/devices/', permanent=True)),I
    
    # Пути для Лабораторной №6
    path('register/', views.register_view, name='register'),
    path('login/', views.login_with_2fa_view, name='login'),
    path('verify-2fa/', views.verify_2fa_view, name='verify_2fa'),
    path('secure/', views.secure_page, name='secure'),     # Защищенная страница
    
    # Выход из системы
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]