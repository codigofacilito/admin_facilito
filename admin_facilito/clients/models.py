#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User

class Client(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE )
	job = models.CharField(max_length=100, default = "")
	bio = models.TextField(max_length=200, default = "")

	def __str__(self):
		return self.user.username

class SocialNetwork(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	facebook = models.URLField( blank=True )
	twitter = models.URLField( blank=True )
	github = models.URLField( blank=True )

	def __str__(self):
		return self.user.username