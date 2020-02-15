from django import forms
from django.forms import RadioSelect

from .constants import rating_choices


class BookAddForm(forms.Form):
    forms.CharField
    title = forms.CharField(max_length=200, label="Title")
    author = forms.CharField(max_length=200, label="Author")
    rating = forms.ChoiceField(widget=RadioSelect, choices=rating_choices)
