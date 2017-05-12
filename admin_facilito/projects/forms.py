#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from .models import Project
from .models import ProjectPermission
import datetime

class ProjectForm(forms.ModelForm):
	title = forms.CharField(label = 'Titulo', required = True)
	description = forms.CharField(label = 'Descripción', required = True, widget=forms.Textarea)
	dead_line = forms.DateField(initial=datetime.date.today)

	class Meta:
		model = Project
		fields = ('title', 'description', 'dead_line')

class PermissionProject(forms.Form):
  permission = forms.ModelChoiceField(
                queryset=ProjectPermission.objects.all(),
                initial=0)

  def __init__(self, *args, **kwargs):
    super(PermissionProject, self).__init__(*args, **kwargs)
    self.fields['permission'].widget.attrs.update( {'class' : 'browser-default'} )