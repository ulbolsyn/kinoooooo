from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password_check=forms.CharField(widget=forms.PasswordInput)
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields=[
        'username',
        'password',
        'password_check',
        'first_name',
        'last_name',
        'email'
        ]
    def __init__(self,*args,**kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Login"
        self.fields['password'].label = "Password"
        self.fields['password'].help_text = "Create a password"
        self.fields['password_check'].label = "Repeat a password"
        self.fields['first_name'].label = "Name"
        self.fields['last_name'].label = "Last_name"
        self.fields['email'].label = "Your Gmail"
        self.fields['email'].help_text = "Please, input a real address"


    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("User with that name is already in the database")
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError("User with that email address  is already in the database")
        if password != password_check:
            raise forms.ValidationError("Passwords do not match. Try again!")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username = username).exists():
            raise forms.ValidationError("User with that name is not registered in the system")

        user = User.objects.get(username = username)
        if user and not user.check_password(password):
            raise forms.ValidationError("Invalid Password")
