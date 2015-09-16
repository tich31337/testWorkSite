# -*- coding: utf-8 -*-
from .models import CustomUser, s_group, s_office, s_timetable, s_fault, s_drop_lift, s_commit
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from datetime import datetime


class AdminUserAddForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # verbose_name = "AdminUserAddForm"
        # verbose_name_plural = "AdminUserAddForms"

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            CustomUser._default_manager.get(username = username)
        except CustomUser.DoesNotExist:
            return username
        raise forms.ValidationsError(self.error_messages['duplicate_username'])


class AdminUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class s_faultForm(forms.ModelForm):
    # error_css_class = 'large-4 medium-4 columns'
    # required_css_class = 'large-4 medium-4 columns'
    # htmlClass = 'large-4 medium-4 columns'
    fault_time = forms.DateTimeField(
        label = 'Время',
        widget = forms.DateTimeInput(attrs = {'type': 'datetime-local',
                                          'value': datetime.now().strftime('%Y-%m-%dT%H:%M'),
                                          # 'class': 'large-4 medium-4 columns',
                                          # 'data-date-time': ''
                                          }))
    description = forms.CharField(widget = forms.Textarea(attrs = {'rows': '2'}), label = 'Описание:', )

    class Meta:
        model = s_fault
        exclude = ('f_staff',)

    # def __init__(self, *args, **kwargs):
    #     super(ModelForm, self).__init__(*args, **kwargs)
    #     # adding css classes to widgets without define the fields:
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'test'
    def as_div(self):
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
            normal_row = u'<div class ="large-4 medium-4 columns">%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div class="hefp-text">%s</div>',
            errors_on_separate_row = False)


class s_drop_liftForm(forms.ModelForm):
    # error_css_class = 'large-4 medium-4 columns'
    # required_css_class = 'large-4 medium-4 columns'
    stop_lift = forms.DateTimeField(
        label = 'Время остановки',
        widget = forms.DateTimeInput(attrs = {
            'type': 'datetime-local',
            # 'value': datetime.now().strftime('%d.%m.%Y %H:%M'),
        },
            # format = '%Y-%m-%dT%H:%M'
        ),
        initial = datetime.now().strftime('%Y-%m-%dT%H:%M'),
        input_formats = '%Y-%m-%dT%H:%M',
    )
    start_lift = forms.DateTimeField(
        label = 'Время запуска',
        # widget = { 'thedate' : html5.DateTimeLocalInput }
        widget = forms.DateTimeInput(attrs = {
            'type': 'datetime-local',
            # 'format': '%Y-%m-%dT%H:%M',
            # 'value': datetime.now().strftime('%d.%m.%Y %H:%M'),
        },
            # format = '%Y-%m-%dT%H:%M',
        ),
        initial = datetime.now().strftime('%Y-%m-%dT%H:%M'),
        input_formats = '%Y-%m-%dT%H:%M',
        # input_formats = settings.DATE_INPUT_FORMATS,
    )
    description = forms.CharField(required = False, widget = forms.Textarea(attrs = {'rows': '2'}),
                                  label = 'Описание:', )

    class Meta:
        model = s_drop_lift
        fields = '__all__'

    # def is_valid(self):
    #     self.start_lift = self.start_lift.strftime('')
    #     obj = super(s_drop_liftForm, self).is_valid()


    def as_div(self):
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
            normal_row = u'<div class ="large-4 medium-4 columns">%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div class="hefp-text">%s</div>',
            errors_on_separate_row = False)


class s_commitForm(forms.ModelForm):
    s_prim = forms.CharField(widget = forms.Textarea(attrs = {'rows': '2'}), label = 'Примечание:', )

    class Meta:
        model = s_commit
        fields = ('s_prim',)


class SMForm(forms.ModelForm):
    error_css_class = 'large-4 medium-4 columns'
    required_css_class = 'large-4 medium-4 columns'

    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'test'

    def as_div(self):
        "Returns this form rendered as HTML <div>s."
        return self._html_output(
            normal_row = u'<div%(html_class_attr)s>%(label)s %(field)s %(help_text)s %(errors)s</div>',
            error_row = u'<div class="error">%s</div>',
            row_ender = '</div>',
            help_text_html = u'<div class="hefp-text">%s</div>',
            errors_on_separate_row = False)
