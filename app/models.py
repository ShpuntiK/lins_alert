# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
	PERIOD_CHOICES = (
		('1', u'Каждый день'),
		('2', u'Раз в неделю'),
		('3', u'Раз в 2 недели'),
		('4', u'Раз в месяц'),
	)

	user = models.OneToOneField(User)
	alert_server_time = models.TimeField()
	start = models.DateField()
	finish = models.DateField()
	period = models.CharField(max_length=1, choices=PERIOD_CHOICES, default='1')
	time = models.TimeField()
	alert_email = models.BooleanField()
	email = models.EmailField(max_length=255, blank=True, null=True)
	alert_sms = models.BooleanField()
	phone = models.CharField(max_length=15, blank=True)