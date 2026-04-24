from django import forms

class AnimalSearchForm(forms.Form):
    query = forms.CharField(label='Search Animals', max_length=100)