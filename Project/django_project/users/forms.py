from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={"class": "my-field"}),
        label="Name",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "my-field"}), label="Passwort"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "my-field"}),
        label="Passwort bestätigen",
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "my-field"}),
        label="Email",
    )
    display_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "my-field"}),
        label="Username",
    )

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data["username"], password=data["password1"], email=data["email"]
        )
        UserProfile.objects.create(user=user, display_name=data["display_name"])
        return user


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(
        required=False, widget=forms.TextInput(attrs={"class": "my-field"})
    )
    display_name = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "my-field",
            }
        ),
    )

    class Meta:
        model = UserProfile
        fields = ["display_name"]
        labels = {"display_name": "Username"}

    def save(self, *args, **kwargs):
        user_profile = super().save(*args, **kwargs)
        email = self.cleaned_data.get("email")
        if email:
            user_profile.user.email = email
            user_profile.user.save()
        return user_profile


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=254, widget=forms.TextInput(attrs={"class": "my-field"})
    )
    password = forms.CharField(
        label="Passwort", widget=forms.PasswordInput(attrs={"class": "my-field"})
    )
