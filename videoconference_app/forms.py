from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import traceback

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1','password2')
    
    def save(self, commit=True):
        try:
            print(f"Creating user with email: {self.cleaned_data['email']}")
            user = super(RegisterForm, self).save(commit=False)
            user.email = self.cleaned_data['email']
            user.username = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            
            # Debug information
            print(f"User object created: username={user.username}, email={user.email}")
            
            if commit:
                print("Saving user to database...")
                user.save()
                print(f"User saved with ID: {user.id}")
            
            return user
        except Exception as e:
            print(f"Error in RegisterForm.save(): {e}")
            print(traceback.format_exc())
            raise
    