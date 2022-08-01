from django import forms
from captcha.fields import CaptchaField
from django.conf import settings
class CaptchaForm(forms.Form):
    captcha=CaptchaField()
    def __init__(self, *args, **kwargs):
        super(CaptchaForm, self).__init__(*args, **kwargs)
        self.fields['captcha'].widget.attrs['placeholder'] = 'Enter the captcha'
        #settings development will return TRUE a str if dev env
        self.fields['captcha'].required = not settings.DEVELOPMENT
