from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegistrationForm, UserProfileForm, CustomerProfileForm
from .models import CustomerProfile

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to JPT Holidays, {user.first_name or user.username}! Your account has been successfully created.")
            return redirect('core:home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_booking_staff or request.user.is_content_manager or request.user.is_admin_owner:
            return redirect('dashboard:index')
        return redirect('accounts:profile')

    next_url = request.GET.get('next', '')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            if next_url:
                return redirect(next_url)
            if user.is_booking_staff or user.is_content_manager or user.is_admin_owner:
                return redirect('dashboard:index')
            return redirect('accounts:profile')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('core:home')

@login_required
def profile_view(request):
    user = request.user
    customer_profile, _ = CustomerProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        profile_form = CustomerProfileForm(request.POST, instance=customer_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Failed to update profile. Please check the form errors.")
    else:
        user_form = UserProfileForm(instance=user)
        profile_form = CustomerProfileForm(instance=customer_profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'customer_profile': customer_profile,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})
