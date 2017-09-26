# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Q
from django.http.request import QueryDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Doctor, Patient

def doctors_list(request):
    
    kwargs = {}
    
    page = request.GET.get('page')
    order = ('last_name',)
    kwargs = get_paginator(Doctor, page, order)
    print kwargs
    doctors = Doctor.objects.all()

    kwargs['no_sidebar'] = True
    #kwargs['key'] = doctors
    kwargs['keys'] = ['last_name','first_name']
    kwargs['title'] = 'Doctores'
    kwargs['suptitle'] = 'Cardiología'

    return render(request, 'doctors_list.html', kwargs)


def patients_list(request):
    
    kwargs = {}
    
    page = request.GET.get('page')
    order = ('last_name',)
    kwargs = get_paginator(Patient, page, order)
    print kwargs
    patients = Patient.objects.all()

    kwargs['no_sidebar'] = True
    #kwargs['key'] = doctors
    kwargs['keys'] = ['last_name','first_name']
    kwargs['title'] = 'Pacientes'
    kwargs['suptitle'] = 'Cardiología'

    return render(request, 'doctors_list.html', kwargs)


def get_paginator(model, page, order, filters={}, n=10):

    kwargs = {}
    query = Q()
    if isinstance(filters, QueryDict):
        filters = filters.dict()
    [filters.pop(key) for key in filters.keys() if filters[key] in ('', ' ')]
    filters.pop('page', None)

    if 'template' in filters:
        filters['template'] = True
    if 'start_date' in filters:
        filters['start_date__gte'] = filters.pop('start_date')
    if 'end_date' in filters:
        filters['start_date__lte'] = filters.pop('end_date')
    if 'tags' in filters:
        tags = filters.pop('tags')
        fields = [f.name for f in model._meta.get_fields()]

        if 'tags' in fields:
            query = query | Q(tags__icontains=tags)
        if 'name' in fields:
            query = query | Q(name__icontains=tags)
        if 'location' in fields:
            query = query | Q(location__name__icontains=tags)
        if 'device' in fields:
            query = query | Q(device__device_type__name__icontains=tags)

    object_list = model.objects.filter(query, **filters).order_by(*order)
    paginator = Paginator(object_list, n)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    kwargs['objects'] = objects
    kwargs['offset'] = (int(page)-1)*n if page else 0

    return kwargs