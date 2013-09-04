#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mass_mail
from django.contrib.auth.models import User
from app.models import Alert
from datetime import datetime, date, timedelta
import requests
import json

def create_email(username, to_email):
	subject = u'LinsAlert - оповещение о смене линз.'
	msg = u'Здравствуйте, ' + username + u'.\n\nСервис LinsAlert напоминает вам о необходимости смены линз.'
	from_email = u'shpuntik74@gmail.com'

	return (subject, msg, from_email, [to_email])

def create_sms(to_phone):
	return {
		'to': to_phone,
		'from': u'LinsAlert',
		'text': u'Сервис LinsAlert напоминает вам о необходимости смены линз.'
	}

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
			email_msg = []
			sms_msg = []
			
			for alert in alerts:
				if alert.alert_email:				
					email_msg.append(create_email(alert.user.first_name, alert.email))
				if alert.alert_sms:
					sms_msg.append(create_sms(alert.phone))

			try:
				send_mass_mail(email_msg, fail_silently=False)
			except Exception as error:
				print 'Email alert error: %s' % CommandError(error)
			try:
				sms_id = '7920'
				sms_key = '4700ABBCB9177DD2'
				headers = {'content-type': 'application/json'}
				r = requests.post('http://bytehand.com:3800/send_multi?id='+sms_id+'&key='+sms_key, data=json.dumps(sms_msg), headers=headers)
			except Exception as error:
				print 'Sms alert error: %s' % r.json()
