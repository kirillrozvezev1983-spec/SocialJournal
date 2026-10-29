from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Post


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", max_length=150)
    email = forms.EmailField(label="Email")
    age = forms.IntegerField(label="Возраст", min_value=1, max_value=120)
    work = forms.CharField(label="Работа", max_length=100)
    hobbies = forms.CharField(label="Увлечения (необязательно)", max_length=250, required=False)

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]
        labels = {"username": "Логин", "password1": "Пароль", "password2": "Повторите пароль"}

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Аккаунт с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                age=self.cleaned_data["age"],
                work=self.cleaned_data["work"],
                hobbies=self.cleaned_data["hobbies"],
            )
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["text"]
        labels = {"text": "О чём хотите рассказать?"}
        widgets = {"text": forms.Textarea(attrs={"placeholder": "Напишите что-нибудь...", "rows": 4, "maxlength": 500})}

    def clean_text(self):
        text = self.cleaned_data["text"].strip()
        if not text:
            raise forms.ValidationError("Пост не может быть пустым.")
        if len(text) > 500:
            raise forms.ValidationError("Максимальная длина поста — 500 символов.")
        return text
