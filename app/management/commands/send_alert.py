#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from app.models import Alert
from datetime import datetime

class Command(BaseCommand):
	args = ''
	help = 'Run alerts for users'

	def handle(self, *args, **options):
		cur_time = datetime.now().strftime('%H:%M')
		alerts = Alert.objects.filter(alert_server_time=cur_time)
		#alerts = Alert.objects.all()

		if alerts.count() != 0:
			msges = []
			
			for alert in alerts:
				subject = u'LinsAlert - оповещение о смене линз.'
				msg = u'Здравствуйте, ' + alert.user.first_name + u'. Сервис LinsAlert напоминает вам об необходимости смены линз.'
				from_email = u'shpuntik74@gmail.com'
				
				msges.append((subject, msg, from_email, [alert.email]))
			
			try:
				send_mass_mail(msges, fail_silently=False)
			except Exception as error:
				print CommandError(error)
