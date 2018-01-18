# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from apps.person.models import Doctor, Patient

import datetime


class Signal(models.Model):
    name             = models.CharField(default='None',max_length=50)
    parameters       = models.TextField(blank=True, null=True)
    acquisition_date = models.DateField('Fecha de Adquisicion', default=datetime.date.today, db_index=True)

    class Meta:
        db_table = 'signals'

    def __str__(self):
        return u'%s, %s' % (self.name, self.acquisition_date)

    def get_diagnosis(self):
        diagnosis=get_object_or_404(Diagnosis, signal=self)
        patient = diagnosis.patient
        return patient.pk



class Diagnosis(models.Model):
    doctor    = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient   = models.ForeignKey(Patient, verbose_name ='Paciente')
    date      = models.DateField('Fecha', default=datetime.date.today, db_index=True)
    signal    = models.ForeignKey(Signal, verbose_name='ECGsignal', null=True, blank=True)
    diagnosis = models.CharField(max_length=200)
    comment   = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'diagnosis'

    def __str__(self):
        return u'%s, %s' % (self.patient, self.diagnosis)

    def get_url_diagnosis_plot(self):
        return reverse('url_diagnosis_plot', args=[self.patient.pk, str(self.pk)])