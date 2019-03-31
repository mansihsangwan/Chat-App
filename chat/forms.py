from django import forms
from .models import ChatMessage
from chat.models import *
from django.contrib.auth.models import User

class ComposeForm(forms.Form):
    message = forms.CharField(
            widget=forms.TextInput(
                attrs={"class": "form-control"}
                )
)
    thumb = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes',
        required = False
    )

class UserListForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields=["user"]


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','password','email')