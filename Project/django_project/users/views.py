from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import UserProfile
from .forms import RegistrationForm, EditProfileForm, LoginForm


# Create your views here.


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("home")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


@login_required
def profile_update_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("users:profile")
    else:
        form = EditProfileForm(instance=profile)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "users/view_profile.html", {"profile": profile})


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect("home")
