# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from __future__ import absolute_import

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Diagnosis, Signal
from .forms import SignalProcessingForm
from .utils.ecg_plotter import plot_ecg

from apps.person.models import Patient

# Create your views here.
def diagnosis_plot(request, patient_id, diag_id):

    diagnosis = get_object_or_404(Diagnosis, pk=diag_id)
    patient   = diagnosis.patient 

    kwargs = {}
    kwargs['patient'] = patient
    kwargs['title']   = 'Diagnosis'
    kwargs['suptitle'] = diagnosis.diagnosis

    return render(request, 'diagnosis_plot.html', kwargs)


class PlotECG(TemplateView):
    template_name = "diagnosis_plot.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        diagnosis = get_object_or_404(Diagnosis, pk=kwargs['diag_id'])
        patient   = diagnosis.patient

        signal_file = diagnosis.signal.name
        plot, values = plot_ecg(diagnosis.signal.name)
        
        if values['FA']:
            result = 'Presencia de Arritmia de Fibrilación auricular'
        else:
            result = 'No se detecta presencia de Fibrilación Auricular'

        kwargs['patient'] = patient
        kwargs['title']   = 'Diagnosis'
        kwargs['suptitle'] = diagnosis.diagnosis
        context = super(PlotECG, self).get_context_data(**kwargs)
        context['plot']          = plot
        context['result']        = result
        context['rateBPM']       = values['rateBPM']
        context['cycles_num']    = values['cycles_num']
        context['cycles']        = values['cycles']
        context['rr_mean']       = values['rr_mean']
        context['up_rr_mean']    = values['up_rr_mean']
        context['down_rr_mean']  = values['down_rr_mean']
        
        return context


def processing_parameters(request, patient_id):

    patient = get_object_or_404(Patient, pk=patient_id)
    signals = Signal.objects.filter(diagnosis__patient=patient)

    if request.method=='GET':
        form = SignalProcessingForm(initial=request.GET,
                                    signal_choices=signals.values_list('pk', 'name'))

    if request.method=='POST':
        data = {'signals': request.POST['signals'], 'blocktime': request.POST['blocktime'], 
                'start_date': request.POST['start_date'], 'end_date': request.POST['end_date']}
       
        form = SignalProcessingForm(data)
        
        #if form.is_valid():
            #print form
        #return redirect('url_processing_plot', patient_id=patient.pk, signal_id=)
        pass

    kwargs = {}
    kwargs['patient']  = patient
    kwargs['title']    = 'Processing'
    kwargs['subtitle'] = 'Parameters'
    kwargs['form']     = form
    kwargs['button']   = 'Process'

    return render(request, 'processing_values.html', kwargs)


def processing_plot(request, patient_id, signal_id):

    patient = get_object_or_404(Patient, pk=patient_id)
    signals = get_object_or_404(Signal, pk=signal_id)

    return HttpResponse("Hello, world. You're at the polls index.")
#return render(request, 'processing_plot.html', kwargs)
    