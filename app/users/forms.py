from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django import forms


from .models import CustomUser, ContactUs, UnregisteredContact


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")


class UserCreateMessageForm(ModelForm):
    class Meta:
        model = ContactUs
        fields = ['user', 'message']
        labels = {
            'message': 'Повідомлення',
        }
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Напишіть своє повідомлення...'}),
        }


class UnregisteredUserCreateMessageForm(ModelForm):
    class Meta:
        model = UnregisteredContact
        fields = ['unregistered_email', 'message']
        labels = {
            'unregistered_email': 'Email:',
            'message': 'Повідомлення',
        }
        widgets = {
            'unregistered_email': forms.EmailInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Ваша електронна пошта...'}),
            'message': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Напишіть своє повідомлення...'}),
        }
