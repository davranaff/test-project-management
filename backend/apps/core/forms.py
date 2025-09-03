from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    username_or_email = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"placeholder": "email or username"}), required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if not username_or_email or not password:
            return cleaned_data

        user = authenticate(username=username_or_email, password=password)

        if user is None:
            raise forms.ValidationError(
                "Invalid username/email or password."
            )

        cleaned_data['user'] = user
        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=False, help_text="Оставьте пустым, если используете email")
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if not username and email:
            cleaned_data['username'] = email

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже занят.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if not user.username:
            user.username = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
