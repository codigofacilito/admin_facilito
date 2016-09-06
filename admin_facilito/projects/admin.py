from django.contrib import admin
from .models import Project
from .models import ProjectStatus
from .models import ProjectPermission
from .models import ProjectUser

class ProjectStatusInLine(admin.TabularInline):
	model =  ProjectStatus
	extra = 0
	can_delete = False

class ProjectAdmin(admin.ModelAdmin):
	inlines = [ ProjectStatusInLine, ]

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectPermission)
admin.site.register(ProjectUser)