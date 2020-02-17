from django import forms
from django.forms import RadioSelect

from .constants import RATING_CHOICES


class BookForm(forms.Form):
    forms.CharField
    title = forms.CharField(max_length=200, label="Title")
    author = forms.CharField(max_length=200, label="Author")
    rating = forms.ChoiceField(widget=RadioSelect, choices=RATING_CHOICES)
    external_id = forms.CharField(max_length=200, label="External ID")
