# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView

from .models import Diagnosis, Signal
from .utils.ecg_plotter import plot_ecg

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

        kwargs['patient'] = patient
        kwargs['title']   = 'Diagnosis'
        kwargs['suptitle'] = diagnosis.diagnosis
        context = super(PlotECG, self).get_context_data(**kwargs)
        context['plot'] = plot_ecg('ecg_xy.csv')
        return context
