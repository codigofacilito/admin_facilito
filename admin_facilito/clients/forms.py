#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from .models import Client
from .models import SocialNetwork

"""
Constants
"""
ERROR_MESSAGE_USER = {'required' : 'El username es requerido', 'unique' : 'El username ya se encuentra registrado', 'invalid': 'El username es incorrecto' }
ERROR_MESSAGE_PASSWORD = {'required' : 'El password es requerido'} 
ERROR_MESSAGE_EMAIL = {'required' : 'El email es requerido', 'invalid': 'Ingrese un correo valido'}


"""
Functions
"""

def must_be_gt(value_password):
	if len(value_password) < 2:
		raise forms.ValidationError('El password debe contener por lo menos 5 caracteres.')

"""
Class
"""

class LoginUserForm(forms.Form):
	username = forms.CharField( max_length = 20)
	password = forms.CharField( max_length = 20, widget = forms.PasswordInput() )

	def __init__(self, *args, **kwargs):
		super(LoginUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update( {'id': 'username_login', 'class': 'input_login' } )
		self.fields['password'].widget.attrs.update( {'id': 'password_login', 'class': 'input_login' } )

class CreateUserForm(forms.ModelForm):
	username = forms.CharField( max_length = 20,  error_messages =  ERROR_MESSAGE_USER  )
	password = forms.CharField( max_length = 20, widget = forms.PasswordInput(), error_messages =  ERROR_MESSAGE_PASSWORD  )
	email = forms.CharField( error_messages =  ERROR_MESSAGE_EMAIL  )

	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update( {'id': 'username_create' } )
		self.fields['password'].widget.attrs.update( {'id': 'password_create' } )
		self.fields['email'].widget.attrs.update( {'id': 'email_create' } )

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).count():
			raise forms.ValidationError('El email debe de ser unico.')
		return email

	class Meta:
		model = User
		fields = ('username', 'password', 'email')

class EditUserForm(forms.ModelForm):
	username = forms.CharField( max_length = 20,  error_messages =  ERROR_MESSAGE_USER  )
	email = forms.CharField( error_messages =  ERROR_MESSAGE_EMAIL  )
	first_name = forms.CharField(label = 'Nombre completo', required=False)
	last_name = forms.CharField(label = 'Apellidos', required=False)

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name' )

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email=email).exclude(pk=self.instance.id).count():
			raise forms.ValidationError('El email debe de ser unico.')
		return email
	
class EditPasswordForm(forms.Form):
	password = forms.CharField( max_length = 20, widget = forms.PasswordInput() )
	new_password = forms.CharField(max_length = 20,label = "Nueva password", widget = forms.PasswordInput(), validators = [must_be_gt]  )
	repeat_password = forms.CharField(max_length = 20,label = "Repetir nueva password", widget = forms.PasswordInput(),  validators = [must_be_gt])

	def clean(self):
		clean_data = super(EditPasswordForm,self).clean()
		password1 = clean_data.get('new_password')
		password2 = clean_data.get('repeat_password')

		if password1 != password2:
			raise forms.ValidationError('Los password no son los mismos')

class EditClientForm(forms.ModelForm):

	job = forms.CharField(label= "Trabajo actual", required=False)
	bio = forms.CharField(label= "Biografía", widget=forms.Textarea, required=False)

	class Meta:
		model = Client
		exclude = ['user']

	def __init__(self, *args, **kwargs):
		super(EditClientForm, self).__init__(*args, **kwargs)
		self.fields['job'].widget.attrs.update({'id': 'job_edit_client', 'class' : 'validate'})
		self.fields['bio'].widget.attrs.update({'id': 'bio_edit_client', 'class' : 'validate'})

class EditClientSocial(forms.ModelForm):
	class Meta:
		model = SocialNetwork
		exclude = ['user']





