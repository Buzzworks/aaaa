from datetime import datetime
import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render

from callcenter.models import AgentActivity

class SessionIdleMiddleware:
	""" 
	checking session details for every request if experied 
	then logout 
	"""
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		csrf_cookie = request.META.get('CSRF_COOKIE')
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		if request.user.is_authenticated:
			if 'usr_csrf_cookie' not in request.session:
				request.session['usr_csrf_cookie'] = csrf_cookie
			else:
				if request.session['usr_csrf_cookie'] != csrf_cookie:
					# print("SecurityError :: Using Unautherized way to access the account by... "+ip+" to the user " + request.user + " to ip " + request.session['ip_address'])
					return render(request, '404.html')
			if 'ip_address' not in request.session:
				request.session['ip_address'] = ip
			else:
				if request.session['ip_address'] != ip:
					print('Network Switch ::',request.session['ip_address'],ip)
					msg_event = 'Network switch - Old IP - '+ request.session['ip_address'] + ' To '+ip
					AgentActivity.objects.create(user = request.user, event = msg_event,event_time = datetime.now())
					request.session['ip_address'] = ip
			if 'last_request' in request.session:
				elapsed = time.time() - request.session['last_request']
				if elapsed > settings.SESSION_IDLE_TIMEOUT:
					del request.session['last_request']
					logout(request)
			request.session['last_request'] = time.time()
		else:
			if 'last_request' in request.session:
				del request.session['last_request']

		response = self.get_response(request)

		return response