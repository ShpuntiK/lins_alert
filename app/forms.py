# -*- coding: utf-8 -*-

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import floppyforms as forms
from models import Alert

RU_ERRORS = {
	'required': u'Заполните поле',
	'invalid': u'Проверьте корретность введенных данных'
}

class SignUpForm(forms.Form):
	username = forms.CharField(error_messages=RU_ERRORS, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Логин', 'autofocus': ''}))
	password = forms.CharField(error_messages=RU_ERRORS, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'Пароль'}))
	password_repeat = forms.CharField(error_messages=RU_ERRORS, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'Повторите пароль'}))

	def clean(self):
		cleaned_data = super(SignUpForm, self).clean()

		password = cleaned_data.get('password')
		password_repeat = cleaned_data.get('password_repeat')

		if password != password_repeat:
			raise forms.ValidationError(u'Пароли не совпадают')

		return cleaned_data

	def clean_username(self):
		username = self.cleaned_data['username']

		if User.objects.filter(username=username).count() != 0:
			raise forms.ValidationError(u'Пользователь с таким логином уже существует')

		return self.cleaned_data

class SignInForm(forms.Form):
	username = forms.CharField(error_messages=RU_ERRORS, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Логин', 'autofocus': ''}))
	password = forms.CharField(error_messages=RU_ERRORS, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': u'Пароль'}))

	def clean(self):
		cleaned_data = super(SignInForm, self).clean()

		if not self.errors:
			user = authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))
			if user is None:
				raise forms.ValidationError(u'Пользователя с таким логином или паролем не существует')
			self.user = user
	
		return cleaned_data

	def get_user(self):
		return self.user or None

class SettingsForm(forms.ModelForm):
	start = forms.DateField(input_formats=('%d.%m.%Y',), error_messages=RU_ERRORS, widget=forms.DateInput(attrs={'class': 'input-small form-control'}))
	finish = forms.DateField(input_formats=('%d.%m.%Y',), error_messages=RU_ERRORS, widget=forms.DateInput(attrs={'class': 'input-small form-control'}))
	time = forms.TimeField(input_formats=('%H:%M',), error_messages=RU_ERRORS, widget=forms.TimeInput(attrs={'class': 'form-control', 'id': 'alert-time-display', 'value': '12:00'}))
	email = forms.EmailField(required=False, error_messages=RU_ERRORS, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': u'Укажите email для оповещений'}))
	user_time = forms.CharField(widget=forms.HiddenInput())

	class Meta:
		model = Alert
		widgets = {
			'alert_email': forms.CheckboxInput(attrs={'id': 'email-alert'}),
			'alert_sms': forms.CheckboxInput(attrs={'disabled': ''}),
			'period': forms.Select(attrs={'class': 'form-control'}),
		}
		exclude = ['user', 'alert_server_time']

	def clean(self):
		cleaned_data = super(SettingsForm, self).clean()

		if cleaned_data.get('alert_email'):
			if cleaned_data.get('email') == '':
				raise forms.ValidationError(u'Введите email')
	
		return cleaned_data

class ContactForm(forms.Form):
	email = forms.CharField(error_messages=RU_ERRORS, widget=forms.EmailInput(attrs={'class': 'form-control'}))
	subject = forms.CharField(error_messages=RU_ERRORS, widget=forms.TextInput(attrs={'class': 'form-control'}))
	message = forms.CharField(error_messages=RU_ERRORS, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 7}))