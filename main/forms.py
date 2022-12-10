from django import forms
from django.forms import ModelForm, Textarea, Select
from .models import *

DAYS = (
    (1, 'День 1'),
    (2, 'День 2'),
    (3, 'День 3'),
    (4, 'День 4'),
)


class EventForm(ModelForm):
    date = forms.DateField(input_formats=['%d/%m/%Y'])
    day = forms.ChoiceField(choices=DAYS, widget=forms.Select(attrs={'class': 'form-control'}))
    text = forms.Textarea()
    workout = forms.ModelChoiceField(queryset=ActiveWorkout.objects.all(),
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Event
        fields = ['date', 'text', 'workout', ]
        widgets = {
            'text': Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
