# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import SignUpForm, SignInForm, SettingsForm, ContactForm
from models import Alert
from datetime import datetime, time, timedelta
import requests

def index(request):
	return render_to_response('index.html', RequestContext(request))

@login_required
def settings(request):
	if request.method == 'POST':
		form = SettingsForm(request.POST)
		if form.is_valid():
			try:
				Alert.objects.get(user=request.user).delete()
			except:
				pass

			data = form.cleaned_data

			client_t = data['user_time']
			server_t = datetime.now().strftime('%H')
			tz_diff = int(server_t) - int(client_t)
			as_time = datetime(2013, 1, 1, data['time'].hour, data['time'].minute)			
			as_time = as_time + timedelta(hours=tz_diff)

			# if data['period'] == '1':
			# 	alert_period = 1
			# elif data['period'] == '2':
			# 	alert_period = 7
			# elif data['period'] == '3':
			# 	alert_period = 14
			# else:
			# 	alert_period = 28

			# print data

			a = Alert(
				user=request.user,
				alert_server_time=as_time,
				start=data['start'],
				finish=data['finish'],
				period=data['period'],
				time=data['time'],
				alert_email=data['alert_email'],
				email=data['email'],
				alert_sms=data['alert_sms'],
				phone=data['phone']
			)

			a.save()
			return HttpResponseRedirect('/settings')
	else:
		try:
			a = Alert.objects.get(user=request.user)
			form = SettingsForm(instance=a)
		except: 
			form = SettingsForm()

	return render_to_response('settings.html', {'form': form}, RequestContext(request))

def contacts(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			pass #send_email
	else:
		form = ContactForm()

	return render_to_response('contacts.html', {'form': form}, RequestContext(request))

def signIn(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == 'POST':
		form = SignInForm(request.POST)
		if form.is_valid():
			if form.get_user():
				login(request, form.get_user())
				return HttpResponseRedirect('/settings')
	else:
		form = SignInForm()

	return render_to_response('sign_in.html', {'form': form}, RequestContext(request))

def signInVk(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == 'GET' and request.GET['code']:
		params = {
			'client_id': '3848319',
			'client_secret': 'hIZ7VPQv3bwfRdcmQxVf',
			'code': request.GET['code'],
			'redirect_uri': 'http://linsalert.mooo.com/sign_in_vk'
		}

		r = requests.get('https://oauth.vk.com/access_token', params=params)
		user_data = r.json()

		r = requests.get('https://api.vk.com/method/users.get?user_ids=' + str(user_data['user_id']))
		user_data = r.json()['response'][0]
		password = user_data['last_name'] + str(user_data['uid'])

		if User.objects.filter(username=user_data['uid']).count() == 0:
			User.objects.create_user(username=user_data['uid'], password=password, first_name=user_data['first_name'])
	
		user = authenticate(username=user_data['uid'], password=password)
		login(request, user)
		
		return HttpResponseRedirect('/settings')

def signUp(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			if User.objects.create_user(username=username, password=password, first_name=username):
				user = authenticate(username=username, password=password)
				login(request, user)
				return HttpResponseRedirect('/settings')
	else:
		form = SignUpForm()

	return render_to_response('sign_up.html', {'form': form}, RequestContext(request))

def signOut(request):
	logout(request)

	return HttpResponseRedirect('/')
