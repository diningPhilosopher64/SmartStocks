from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Financials

class RegisterUser(UserCreationForm):
        first_name =  forms.CharField( max_length=50, required=True)
        last_name =  forms.CharField(max_length=50, required=True)   
        email = forms.EmailField( required=True)
        account_num = forms.IntegerField(required=True)
        balance=forms.DecimalField(required=True)
        class Meta:
            model = User
            fields = ("first_name", "last_name","username", "email","password1","password2")    

        def save(self, commit=True):
            user = super(RegisterUser, self).save(commit=False)
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            fin=Financials()
            fin.user=user
            fin.account_num= self.cleaned_data['account_num']
            fin.balance= self.cleaned_data['balance']
            if commit:
                user.save()
                fin.save()
            return user



