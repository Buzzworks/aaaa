from django.http import JsonResponse
from .models import CrmField, Phonebook
import json
import os
from django.conf import settings

def crm_field_validation(function):
	"""
	This validation is used to do validation of
	crm field is already exist or not with same detail
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk", "")
		name = request.POST["name"]
		if pk:
			crm_field = CrmField.objects.filter(name__iexact=name).exclude(
					id=pk).exists()
		else:
			crm_field = CrmField.objects.filter(name__iexact=name).exists()

		if crm_field:
			return JsonResponse(
				{"name": "CrmField with the given name already exists"},
				status=500)
		return function(request, *args, **kwargs)
	return wrap

def phonebook_validation(function):
	"""
	this decorator is a phonebook validator
	"""
	def wrap(request, *args, **kwargs):
		pk = kwargs.get("pk","")
		name = request.POST["name"]
		uploaded_file = request.FILES.get("uploaded_file", "")
		if pk:
			ph_name = Phonebook.objects.filter(name__iexact=name).exclude(id=pk).exists()
		else:
			ph_name = Phonebook.objects.filter(name__iexact=name).exists()
		if ph_name:
			return JsonResponse({"errors":"Phonebook with this name already Exists"},status=500)
		return function(request, *args, **kwargs)
	return wrap

