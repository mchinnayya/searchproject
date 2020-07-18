from django import forms
from django.contrib.auth.models import User

from account.models import Account

choice = [('0', 'admin'), ('1', 'user'), ]
activeChoice = [('0', 'Inactive'), ('1', 'Active'), ]


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class AccountForm(forms.ModelForm):
    active = forms.IntegerField(label="Status", required=True, widget=forms.Select(choices=activeChoice,
                                                                                   attrs={
                                                                                       'class': 'form-control'}))  # 1 means Active, 0 means Inactive
    role = forms.CharField(label='Role', required=True,
                           widget=forms.Select(choices=choice, attrs={'class': 'form-control'}))

    class Meta:
        model = Account
        fields = ('active', 'role',)
