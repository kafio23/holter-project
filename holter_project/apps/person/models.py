# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, UserManager
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from django.db import models

import datetime

class Doctor(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='doctor')
    last_name = models.CharField(verbose_name='Apellido Paterno', max_length=50)
    second_last_name = models.CharField(verbose_name='Apellido Materno', max_length=32, blank=True, null=True)
    first_name = models.CharField(verbose_name='Primer Nombre', max_length=50)
    second_name = models.CharField(verbose_name='Segundo Nombre', max_length=32, blank=True, null=True)
    dni = models.CharField(verbose_name='DNI', max_length=32)
    date_of_birth = models.DateField('Fecha de Nacimiento', default=datetime.date.today, db_index=True)

    class Meta:
        db_table = 'doctor_users'

    def __str__(self):
        return u'%s, %s' % (self.last_name, self.first_name)


class Patient(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='patient')
    last_name = models.CharField(verbose_name='Apellido Paterno', max_length=50)
    second_last_name = models.CharField(verbose_name='Apellido Materno', max_length=32, blank=True, null=True)
    first_name = models.CharField(verbose_name='Primer Nombre', max_length=50)
    second_name = models.CharField(verbose_name='Segundo Nombre', max_length=32, blank=True, null=True)
    dni = models.CharField(verbose_name='DNI', max_length=32)
    date_of_birth = models.DateField('Fecha de Nacimiento', default=datetime.date.today, db_index=True)

    class Meta:
        db_table = 'patient_users'

    def get_absolute_url(self):
        return reverse('url_patient_view', args=[str(self.pk)])