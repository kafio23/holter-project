from __future__ import absolute_import

from django import forms
from django.utils.safestring import mark_safe

from .models import Signal
from apps.person.models import Patient

BLOCKTIME_SECS = (
                (10, '10'),
                (20, '20'),
                (60, '60'),                
                )


class DateRangepickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        html = '''<div class="col-md-4 input-group date" id="datetimepicker1" style="float:inherit">
        <input class="form-control" id="id_start_date" name="start_date" placeholder="Start" title="" type="text">
        <span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>
        </div>
        <br>
        <div class="col-md-4 input-group date" id="datetimepicker2" style="float:inherit">
        <input class="form-control" id="id_end_date" name="end_date" placeholder="End" title="" type="text">
        <span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span>
        </div>'''
        return mark_safe(html)


class SignalProcessingForm(forms.Form):

    signals    = forms.ChoiceField(label="Signals")
    blocktime  = forms.ChoiceField(label="Secs per Block", choices=BLOCKTIME_SECS) #blocktime  = forms.IntegerField(label="Segundos por Bloque", min_value=10)
    range_date = forms.DateTimeField(label="DateTime Selector")

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields', [])
        signal_choices = kwargs.pop('signal_choices', [])
        super(SignalProcessingForm, self).__init__(*args, **kwargs)

        self.fields['signals'].choices = signal_choices
        self.fields['range_date'].widget = DateRangepickerWidget()