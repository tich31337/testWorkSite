# -*- coding: utf-8 -*-
from .models import User, s_group, s_office, s_timetable
from django import forms 
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class AdminUserAddForm(UserCreationForm):

    class Meta:
        model = User
        # verbose_name = "AdminUserAddForm"
        # verbose_name_plural = "AdminUserAddForms"

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationsError(self.error_messages['duplicate_username'])

class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = User
    