from django import forms
from .models import Destination, Review
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = ['name', 'location', 'description', 'category', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            'category': forms.Select(choices=[('beach', 'Beach'), ('mountain', 'Mountain'), ('city', 'City'), ('historical', 'Historical'), ('food', 'Food'), ('drink', 'Drink')]),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'review', 'title', 'image', 'pros', 'cons']
        widgets = {
            'rating': forms.HiddenInput(),  # We'll handle this with custom JavaScript
            'review': forms.Textarea(attrs={'rows': 3, 'cols': 50, 'class': 'form-control'}),
            'pros': forms.Textarea(attrs={'rows': 2, 'cols': 50, 'class': 'form-control'}),
            'cons': forms.Textarea(attrs={'rows': 2, 'cols': 50, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }


class ProfileEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username']  # List only fields you want to allow updating

class PasswordUpdateForm(PasswordChangeForm):
    pass  # This uses the built-in PasswordChangeForm as is

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100, label='Search')