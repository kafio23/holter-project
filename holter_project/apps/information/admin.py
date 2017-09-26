# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Diagnosis, Signal

admin.site.register(Diagnosis)
admin.site.register(Signal)