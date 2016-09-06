from django.shortcuts import render
from django.shortcuts import get_object_or_404

from status.models import Status
from .models import Project
from .models import ProjectUser
from .forms import ProjectForm
from status.forms import StatusChoiceForm

from django.views.generic.list import ListView
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from django.contrib import messages
from django.db import transaction

"""
Class
"""
class CreateClass(CreateView,LoginRequiredMixin):
	login_url = 'client_login'
	template_name = 'project/create.html'
	model = Project
	form_class = ProjectForm

	@transaction.atomic
	def create_objects(self):
		self.object.save()
		self.object.projectstatus_set.create( status = Status.get_defult_status() )
		self.object.projectuser_set.create(user= self.request.user, permission_id = 1 )

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.create_objects()
		return HttpResponseRedirect( self.get_url_project() )

	def get_url_project(self):
		return reverse_lazy('project:show', kwargs = {'slug' : self.object.slug} )

class ListClass(ListView, LoginRequiredMixin):
	login_url = 'client_login'
	template_name = 'project/own.html'

	def get_queryset(self):
		return ProjectUser.objects.filter(user = self.request.user)

class ShowClass(DetailView):
	model = Project
	template_name = 'project/show.html'

"""
Functions
"""
@login_required(login_url='client:login')
def edit(request, slug=''):
	project = get_object_or_404(Project, slug=slug)
	
	form_project = ProjectForm(request.POST or None, instance = project)
	forms_status = StatusChoiceForm(request.POST or None, 
									initial = {'status': project.get_id_status()
								})

	if request.method == 'POST':
		if form_project.is_valid() and forms_status.is_valid():
			selection_id = forms_status.cleaned_data['status'].id

			form_project.save()
			if selection_id != project.get_id_status():
				project.projectstatus_set.create( status_id = selection_id)
			messages.success(request, 'Datos actualizados correctamente')
	context = {
		'form_project': form_project,
		'forms_status': forms_status
	}
	return render(request, 'project/edit.html', context)
