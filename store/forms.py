from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from store.models import Customer, User


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('phone', 'country', 'city',
                  'region', 'street', 'postal_office')


class UserPasswordChangeForm(PasswordChangeForm):
    pass
