from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import traceback

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "input"})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={"class": "input"})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "input"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        required=True,
        widget=forms.PasswordInput(attrs={"class": "input"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def save(self, commit=True):
        print(f"DEBUG RegisterForm.save() - Creating user with email: {self.cleaned_data['email']}, username: {self.cleaned_data['username']}")
        try:
            # Set username to email to ensure we can look up users consistently
            self.instance.username = self.cleaned_data['email']
            self.instance.email = self.cleaned_data['email']
            
            # Get first_name and last_name from the form data if available
            first_name = self.data.get('first_name', '')
            last_name = self.data.get('last_name', '')
            
            if first_name:
                self.instance.first_name = first_name
            if last_name:
                self.instance.last_name = last_name
                
            user = super().save(commit=commit)
            print(f"DEBUG RegisterForm.save() - User saved successfully. ID: {user.id}")
            return user
        except Exception as e:
            print(f"DEBUG RegisterForm.save() - Error: {str(e)}")
            raise
    