import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Device
from .serializers import DeviceSerializer

# 1. Твій вчорашній API (LBA 5) — ОБОВ'ЯЗКОВО МАЄ БУТИ ТУТ
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

# 2. Реєстрація користувача (LBA 6)
def register_view(request):
    if request.method == 'POST':
        # Створення користувача через ORM для захисту від SQL Injection 
        User.objects.create_user(
            username=request.POST['username'],
            email=request.POST['email'],
            password=request.POST['password']
        )
        return redirect('login')
    return render(request, 'register.html')

# 3. Вхід з імітацією 2FA (LBA 6) [cite: 107]
def login_with_2fa_view(request):
    error_message = "Невірний ємейл або пароль" # Готовим текст заранее
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # 1. Пытаемся найти пользователя по Email
        user_obj = User.objects.filter(email=email).first()
        
        if user_obj:
            # 2. Если нашли, проверяем пароль
            user = authenticate(username=user_obj.username, password=password)
            
            if user is not None:
                # 3. ВСЁ ВЕРНО -> Генерируем код
                code = str(random.randint(1000, 9999))
                request.session['pre_2fa_user_id'] = user.id
                request.session['2fa_code'] = code
                print(f"\n=== КОД ПІДТВЕРДЖЕННЯ: {code} ===\n")
                return redirect('verify_2fa')
        
        # Если код не зашел в "if user is not None", значит была ошибка
        return render(request, 'login.html', {'error': error_message})
            
    return render(request, 'login.html')

# 4. Перевірка коду 2FA
def verify_2fa_view(request):
    if request.method == 'POST':
        user_id = request.session.get('pre_2fa_user_id')
        user_code = request.POST.get('code')
        saved_code = request.session.get('2fa_code')
        
        if saved_code == user_code:
            user = User.objects.get(id=user_id)
            auth_login(request, user) # Остаточна автентифікація 
            return redirect('secure')
            
    return render(request, '2fa.html')

# 5. Захищена сторінка (LBA 6) [cite: 86]
@login_required
def secure_page(request):
    return render(request, 'secure.html')