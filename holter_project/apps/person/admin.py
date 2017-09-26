# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Doctor, Patient

admin.site.register(Doctor)
admin.site.register(Patient)