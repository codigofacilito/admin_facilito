from __future__ import unicode_literals

from django.db import models

class Client(models.Model):
	bio = models.TextField(max_length = 200) #Description
	job = models.TextField(max_length = 50 ) #Job
