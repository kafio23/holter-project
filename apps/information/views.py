# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from __future__ import absolute_import

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse
from django.contrib import messages

from .models import Diagnosis, Signal
from .forms import SignalProcessingForm, DiagnosisForm, SignalForm
from .utils.ecg_plotter import signal_processing

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


def diagnosis_edit(request, patient_id, diag_id):
    diagnosis = get_object_or_404(Diagnosis, pk=diag_id)
    patient   = diagnosis.patient 

    if request.method=='GET':
        form = DiagnosisForm(instance=diagnosis)
        signal_form = SignalForm(instance=diagnosis.signal)
    
    if request.method=='POST':
        form = DiagnosisForm(request.POST, instance=diagnosis)
        signal_form = SignalForm(request.POST, instance=diagnosis.signal)
        if signal_form.is_valid():
            updated_signal = signal_form.save(commit=False)
            updated_signal.save()
        if form.is_valid():
            updated_diagnosis = form.save(commit=False)
            updated_diagnosis.save()
            return redirect('url_patient_overview', patient_id=patient.pk)

    kwargs = {}
    kwargs['patient']     = patient
    kwargs['title']       = 'Diagnosis'
    kwargs['suptitle']    = diagnosis.date
    kwargs['form']        = form
    kwargs['signal_form'] = signal_form

    return render(request, 'diagnosis_edit.html', kwargs)


class PlotECG(TemplateView):
    template_name = "diagnosis_plot.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        diagnosis = get_object_or_404(Diagnosis, pk=kwargs['diag_id'])
        patient   = diagnosis.patient

        signal_file = diagnosis.signal.name
        
        plot, values = signal_processing(signal_file)
        plot_message = 'Peligro: '

        plot_message = False
        if not values['suficiente_tiempo']:
            plot_message = 'No se adquirio suficiente tiempo'
        
        if values['ARRITMIA_GENERAL']:
            result = 'Posible presencia de Evento Arritmico'
        else:
            result = 'No se detecta presencia de Evento Arritmico'

        kwargs['patient'] = patient
        kwargs['diagnosis'] = diagnosis
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

        context['plot_message']  = plot_message
        
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
        pass
    kwargs = {}
    kwargs['patient']  = patient
    kwargs['title']    = 'Processing'
    kwargs['subtitle'] = 'Parameters'
    kwargs['form']     = form
    kwargs['button']   = 'Process'

    return render(request, 'processing_values.html', kwargs)


#def processing_plot(request, patient_id, signal_id):

#    patient = get_object_or_404(Patient, pk=patient_id)
#    signals = get_object_or_404(Signal, pk=signal_id)

#    return HttpResponse("Hello, world. You're at the polls index.")


class PlotsECG(TemplateView):
    template_name = "processing_plots.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        diagnosis = get_object_or_404(Diagnosis, pk=kwargs['diag_id'])
        patient   = diagnosis.patient

        signal_file = diagnosis.signal.name
        
        plot, values, event_plots = signal_processing(signal_file, divide_plots=True)
        plot_message = 'Peligro: '
        
        
        if values['FA']:
            result = 'Presencia de Evento: Posible Arritmia de Fibrilación auricular'
        else:
            result = 'No se detecta presencia de Evento de Fibrilación Auricular'

        plot_message = False
        if not values['suficiente_tiempo']:
            plot_message = 'No se adquirio suficiente tiempo'

        if values['ARRITMIA']:
            print('ARRITMIA')

        kwargs['patient'] = patient
        kwargs['diagnosis'] = diagnosis
        kwargs['title']   = 'Diagnosis'
        kwargs['suptitle'] = diagnosis.diagnosis
        context = super(PlotsECG, self).get_context_data(**kwargs)
        context['plot']          = plot
        context['event_plots']   = event_plots
        context['result']        = result
        context['rateBPM']       = values['rateBPM']
        context['cycles_num']    = values['cycles_num']
        context['tiempos_plots'] = values['tiempos_plots']

        context['eventos_num'] = []
        if values['tiempos_plots']:
            context['eventos_num'] = len(values['tiempos_plots'])    

        context['plot_message']  = plot_message        
        
        return context
    