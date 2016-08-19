#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import Project
import datetime

class ProjectForm(forms.ModelForm):
	title = forms.CharField(label = 'Titulo', required = True)
	description = forms.CharField(label = 'Descripción', required = True, widget=forms.Textarea)
	dead_line = forms.DateField(initial=datetime.date.today)

	class Meta:
		model = Project
		fields = ('title', 'description', 'dead_line')