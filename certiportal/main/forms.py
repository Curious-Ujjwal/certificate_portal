from django import forms
from .choices import *
from django.core.validators import RegexValidator
alcher_id_validator = RegexValidator(r"ALC-[A-Z]{3}-[0-9]+", "Alcher ID should be of the form ALC-AAA-12")

class CandidForm(forms.Form):
    alcher_id = forms.CharField(max_length=20, validators = [alcher_id_validator])
    name = forms.CharField(max_length=100)
    event = forms.CharField(
        max_length=20,
        widget=forms.Select(choices=EVENT_OPTIONS),
    )
    certificate_type = forms.CharField(
        max_length=2,
        widget=forms.Select(choices=CERTIFICATE_OPTIONS),
    )



