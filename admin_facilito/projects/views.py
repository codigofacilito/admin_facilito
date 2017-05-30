from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from status.models import Status
from django.contrib.auth.models import User
from .models import Project
from .models import ProjectUser
from .models import ProjectPermission

from .forms import ProjectForm
from .forms import PermissionProject
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
class CreateClass(LoginRequiredMixin, CreateView):
	login_url = 'client:login'
	template_name = 'project/create.html'
	model = Project
	form_class = ProjectForm

	@transaction.atomic
	def create_objects(self):
		self.object.save()
		self.object.projectstatus_set.create( status = Status.get_defult_status() )
		self.object.projectuser_set.create(user= self.request.user,
																			permission=ProjectPermission.founder_permission() )

	def form_valid(self, form):
		self.object = form.save(commit = False)
		self.create_objects()
		return HttpResponseRedirect( self.get_url_project() )

	def get_url_project(self):
		return reverse_lazy('project:show', kwargs = {'slug' : self.object.slug} )

class ListClass(LoginRequiredMixin, ListView):
	login_url = 'client:login'
	template_name = 'project/index.html'

	def get_queryset(self):
		return Project.objects.all()

class ListMyProjectsClass(LoginRequiredMixin, ListView):
	login_url = 'client:login'
	template_name = 'project/mine.html'

	def get_queryset(self):
		return ProjectUser.objects.filter(user = self.request.user)

class ListContributorsClass(ListView):
	template_name = 'project/contributors.html'

	def get_queryset(self):
		self.project = get_object_or_404(Project, slug=self.kwargs['slug'])
		return ProjectUser.objects.filter(project=self.project)

	def get_context_data(self, **kwargs):
		context = super(ListContributorsClass, self).get_context_data(**kwargs)
		context['project'] = self.project
		return context

class ShowClass(DetailView):
	model = Project
	template_name = 'project/show.html'

	def get_context_data(self, **kwargs):
		context = super(ShowClass, self).get_context_data(**kwargs)
		if not self.request.user.is_anonymous():
			context['has_permission'] = self.object.user_has_permission(self.request.user)

		return context

"""
Functions
"""

def admin_only(function):  
	def wrap(request, *args, **kwargs):
	  project = get_object_or_404(Project,slug=kwargs['slug'])
	  if not project.user_has_permission(request.user):
	  	lazy = reverse_lazy('project:show', kwargs={'slug': project.slug})
	  	return HttpResponseRedirect(lazy)
	  return function(request, *args, **kwargs)
	return wrap

@login_required(login_url='client:login')
@admin_only
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

@login_required(login_url='client:login')
@admin_only
def add_contributor(request, slug, username):
	project = get_object_or_404(Project, slug=slug)
	user = get_object_or_404(User, username=username)

	if not project.projectuser_set.filter(user=user).exists():
		project.projectuser_set.create(user=user,
																	permission=ProjectPermission.contributor_permission())

	return redirect('project:contributors', slug=project.slug)

@login_required(login_url='client:login')
def user_contributor(request, slug, username):
	project = get_object_or_404(Project, slug=slug)
	user = get_object_or_404(User, username=username)
	permission = get_object_or_404(ProjectUser, user=user, project=project)

	form = PermissionProject(request.POST or None,
													initial={'permission' : permission.permission_id })

	if request.method == 'POST' and form.is_valid():
		selection_id = form.cleaned_data['permission'].id
		if selection_id != permission.id: #
			permission.permission_id = selection_id
			permission.save()
			messages.success(request, 'Datos actualizados correctamente.')

	context = {
		'project' : project,
		'user' : user,
		'has_permission' : project.user_has_permission(request.user),
		'form' : form,
	}

	return render(request, 'project/contributor.html', context)

@login_required(login_url='client:login')
@admin_only
def delete_contributor(request, slug, username):
	project = get_object_or_404(Project, slug=slug)
	user = get_object_or_404(User, username=username)

	project_user = get_object_or_404(ProjectUser, user=user, project=project)
	if not project_user.is_founder():
		project_user.delete()
	
	return redirect('project:contributors', slug=project.slug)


