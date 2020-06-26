from django import forms

class SuggestionDateForm(forms.Form):
    date = forms.DateField()
