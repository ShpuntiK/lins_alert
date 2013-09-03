#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from app.models import Alert
from datetime import datetime, date, timedelta

class Command(BaseCommand):
	args = ''
	help = 'Send alerts for users'

	def handle(self, *args, **options):
		cur_time = datetime.now().strftime('%H:%M')
		cur_date = date.today()
		pre_alerts = Alert.objects.filter(alert_server_time=cur_time, start__lte=cur_date, finish__gte=cur_date)
		alerts = []

		for alert in pre_alerts:
			real_period = {'1': 1, '2': 7, '3': 14, '4': 28}
			t_date = alert.start
			
			while t_date <= cur_date:
				if t_date == cur_date:
					alerts.append(alert)
					break
				else:
					t_date += timedelta(days=real_period[alert.period])
		
		if len(alerts) != 0:
			msges = []
			
			for alert in alerts:
				subject = u'LinsAlert - оповещение о смене линз.'
				msg = u'Здравствуйте, ' + alert.user.first_name + u'.\n\n Сервис LinsAlert напоминает вам об необходимости смены линз.'
				from_email = u'shpuntik74@gmail.com'
				
				msges.append((subject, msg, from_email, [alert.email]))
			
			try:
				send_mass_mail(msges, fail_silently=False)
			except Exception as error:
				print CommandError(error)
