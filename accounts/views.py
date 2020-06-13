from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.views.decorators.http import require_POST

from .forms import CustomUserCreationForm, CustomUserChangeForm


User = get_user_model()

@login_required
def profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'accounts/profile.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('community:community')
    else:
        form = AuthenticationForm(request)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.created()
            auth_login(request, user)
            return redirect('community:community')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('community:community')

@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)

@login_required
@require_POST
def delete(request):
    user = request.user
    user.delete()
    return redirect('community:community')

@login_required
def change_password(request):
    if request.method == 'POST':
        user = request.user
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/form.html', context)
