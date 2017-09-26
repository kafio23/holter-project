# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
from __future__ import absolute_import

from django.db import models
from apps.person.models import Doctor, Patient

import datetime


class Signal(models.Model):
    values  = models.TextField(blank=True, null=True)
    acquisition_date = models.DateField('Fecha de Adquisicion', default=datetime.date.today, db_index=True)

    class Meta:
        db_table = 'signals'


class Diagnosis(models.Model):
    doctor = models.ForeignKey(Doctor, verbose_name='Doctor')
    patient = models.ForeignKey(Patient, verbose_name ='Paciente')
    date = models.DateField('Fecha', default=datetime.date.today, db_index=True)
    signal = models.ForeignKey(Signal, verbose_name='ECG')
    diagnosis = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'diagnosis'