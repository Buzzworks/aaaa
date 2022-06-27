import time
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import render

class SessionIdleMiddleware:
	""" 
	checking session details for every request if experied 
	then logout 
	"""
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		if request.user.is_authenticated:
			# if 'ip_address' not in request.session:
			# 	request.session['ip_address'] = ip
			# else:
			# 	if request.session['ip_address'] != ip:
			# 		# print("SecurityError :: Using Unautherized way to access the account by... "+ip+" to the user " + request.user + " to ip " + request.session['ip_address'])
			# 		return render(request, '404.html')
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