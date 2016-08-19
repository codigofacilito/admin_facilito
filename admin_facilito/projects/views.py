from django.shortcuts import render

from .models import Project
from .forms import ProjectForm

from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

# Create your views here.
class CreateClass(CreateView,LoginRequiredMixin):
	success_url = reverse_lazy('client:dashboard')

	login_url = 'client_login'
	template_name = 'project/create.html'#Esta pendiente
	model = Project
	form_class = ProjectForm

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.object.user = self.request.user
		self.object.save()
		return HttpResponseRedirect( self.get_success_url() )

class ListClass(ListView, LoginRequiredMixin):
	login_url = 'client_login'
	template_name = 'project/own.html'

	def get_queryset(self):
		return Project.objects.filter(user = self.request.user).order_by('dead_line')

class ShowClass(DetailView):
	model = Project
	template_name = 'project/show.html'






		