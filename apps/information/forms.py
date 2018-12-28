from django import forms
from django.utils.safestring import mark_safe

from .models import Signal, Diagnosis
from apps.person.models import Patient

BLOCKTIME_SECS = (
                (10, '10'),
                (20, '20'),
                (60, '60'),                
                )

class DiagnosisForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiagnosisForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Diagnosis
        fields = ['patient', 'date', 'signal', 'diagnosis', 'comment']


class SignalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SignalForm, self).__init__(*args, **kwargs)
    
    class Meta:
        model = Signal
        fields = ['parameters']


class DatepickerWidget(forms.widgets.TextInput):
    def render(self, name, value, attrs=None):
        input_html = super(DatepickerWidget, self).render(name, value, attrs)
        html = '''<div class="col-md-4 input-group date" id="{}">'''.format(name)
        html += input_html+'<span class="input-group-addon"><i class="glyphicon glyphicon-calendar"></i></span></div>'
        return mark_safe(html)



class SignalProcessingForm(forms.Form):

    signals    = forms.ChoiceField(label="Signals")
    blocktime  = forms.ChoiceField(label="Secs per Block", choices=BLOCKTIME_SECS) #blocktime  = forms.IntegerField(label="Segundos por Bloque", min_value=10)
    start_date = forms.DateTimeField(label="Start Date")
    end_date = forms.DateTimeField(label="End Date")

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields', [])
        signal_choices = kwargs.pop('signal_choices', [])
        super(SignalProcessingForm, self).__init__(*args, **kwargs)

        self.fields['signals'].choices = signal_choices
        self.fields['start_date'].widget = DatepickerWidget(self.fields['start_date'].widget.attrs)
        self.fields['end_date'].widget = DatepickerWidget(self.fields['end_date'].widget.attrs)