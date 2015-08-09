# -*- coding: utf-8 -*-
from .models import CustomUser, s_group, s_office, s_timetable, s_fault, s_drop_lift, s_commit
from django import forms 
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from datetime import datetime


class AdminUserAddForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields  = '__all__'
        # verbose_name = "AdminUserAddForm"
        # verbose_name_plural = "AdminUserAddForms"

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            CustomUser._default_manager.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationsError(self.error_messages['duplicate_username'])

class AdminUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields  = '__all__'

class s_faultForm(forms.ModelForm):
    fault_time = forms.DateTimeField(label='Время', widget=forms.TextInput(attrs={'type': 'datetime-local', 'value': '10. 08. 2015 10:00'}))
    class Meta:
        model = s_fault
        exclude = ('f_staff',)

class s_drop_liftForm(forms.ModelForm):
    stop_lift = forms.DateTimeField(label = 'Время остановки', widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    start_lift = forms.DateTimeField(label = 'Время запуска', widget=forms.TextInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model   = s_drop_lift
        fields  = '__all__'


class s_commitForm(forms.ModelForm):
    class Meta:
        model = s_commit
        fields = ('s_prim',)

