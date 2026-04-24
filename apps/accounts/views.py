"""
Accounts Views: Login, Register, Profile, Logout
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Address


def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username}!")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, "Login yoki parol noto'g'ri.")

    return render(request, 'accounts/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        phone = request.POST.get('phone', '').strip()

        if password != password2:
            messages.error(request, "Parollar mos kelmadi.")
        elif CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu username allaqachon band.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Bu email allaqachon ro'yxatdan o'tgan.")
        else:
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password, phone=phone
            )
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz!")
            return redirect('catalog:home')

    return render(request, 'accounts/register.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Tizimdan chiqdingiz.")
    return redirect('catalog:home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone = request.POST.get('phone', '')
        user.save()
        messages.success(request, "Profil yangilandi.")
        return redirect('accounts:profile')

    orders = request.user.orders.order_by('-created_at')[:5]
    addresses = request.user.addresses.all()
    wishlist = request.user.wishlist.select_related('product')[:10]

    return render(request, 'accounts/profile.html', {
        'orders': orders,
        'addresses': addresses,
        'wishlist': wishlist,
    })
