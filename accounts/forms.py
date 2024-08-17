from django import forms
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input mb-2'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input mb-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-input mb-2'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-input mb-2'}),
            'address': forms.Textarea(attrs={'class': 'form-input mb-2'}),
            'hobby': forms.TextInput(attrs={'class': 'form-input mb-2'}),
        }
