from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http.request import QueryDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .models import Doctor, Patient
from .forms import UploadFileForm
from apps.information.models import Diagnosis, Signal

def doctors_list(request):

    kwargs = {}

    page = request.GET.get('page')
    order = ('last_name',)
    kwargs = get_paginator(Doctor, page, order)
    print(kwargs)
    doctors = Doctor.objects.all()

    kwargs['no_sidebar'] = True
    kwargs['keys'] = ['last_name','first_name']
    kwargs['title'] = 'Doctores'
    kwargs['suptitle'] = 'Cardiología'

    return render(request, 'person/doctors_list.html', kwargs)


def patients_list(request):

    kwargs = {}

    page = request.GET.get('page')
    order = ('last_name',)
    kwargs = get_paginator(Patient, page, order)
    print(kwargs)
    patients = Patient.objects.all()

    kwargs['no_sidebar'] = True
    kwargs['keys'] = ['last_name','first_name']
    kwargs['title'] = 'Pacientes'
    kwargs['suptitle'] = 'Cardiología'

    return render(request, 'person/patients_list.html', kwargs)


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


def patient_view(request, patient_id):

    patient = get_object_or_404(Patient, pk=patient_id)

    kwargs = {}
    kwargs['patient'] = patient
    kwargs['title']   = 'Patient'
    kwargs['suptitle'] = patient
    kwargs['no_sidebar'] = True

    return render(request, 'person/patient.html', kwargs)


def patient_overview(request, patient_id):

    patient   = get_object_or_404(Patient, pk=patient_id)
    diagnosis = Diagnosis.objects.filter(patient=patient)

    kwargs = {}
    kwargs['patient'] = patient
    kwargs['objects'] = diagnosis
    kwargs['title']   = 'Overview'
    kwargs['suptitle'] = patient.first_name+' '+patient.last_name
    kwargs['keys'] = ['doctor', 'diagnosis', 'signal', 'date']
    kwargs['no_sidebar'] = True

    return render(request, 'person/patient_overview.html', kwargs)


def patient_upload(request, patient_id):

    patient = get_object_or_404(Patient, pk=patient_id)
    doctors  = Doctor.objects.all()
    doctor = doctors[0]

    if request.method == 'POST' and request.FILES['file']:

        form = UploadFileForm(request.POST, request.FILES)
        path = 'data/'

        if form.is_valid():
            myfile   = request.FILES['file']

            if myfile.name[-4:] == '.csv' or myfile.name[-4:] == '.txt' :
                print('SI .cvs or .txt')
            else:
                messages.error(request, 'Ingresar archivo con formato valido (.csv)')
                return HttpResponseRedirect(reverse('url_patient_upload', args=[patient_id]))

            fs = FileSystemStorage()
            filename = fs.save(path+myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            new_signal = Signal(name=myfile.name, parameters='')
            new_signal.save()
            new_diagnosis = Diagnosis(doctor=doctor, patient=patient, signal=new_signal, diagnosis='Ingresar diagnostico:...')
            new_diagnosis.save()

            messages.success(request, 'Archivo añadido a la base de datos')
            return HttpResponseRedirect(reverse('url_patient_overview', args=[patient_id]))
        else:
            messages.error(request, 'Ingresar archivo con formato valido')
            return HttpResponseRedirect(reverse('url_patient_view', args=[patient_id]))
    else:
        form = UploadFileForm()

    kwargs = {}
    kwargs['patient']  = patient
    kwargs['title']    = patient.last_name
    kwargs['suptitle'] = patient.first_name
    kwargs['form']     = form
    kwargs['button']   = 'Upload'
    kwargs['no_sidebar'] = True

    return render(request, 'person/patient_upload.html', kwargs)



def upload_file(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})



def signal_upload(request, patient_id):

    patient = get_object_or_404(Patient, pk=patient_id)
    doctors  = Doctor.objects.all()
    doctor = doctors[0]

    if request.method == 'POST' and request.FILES['file']:

        form = UploadFileForm(request.POST, request.FILES)
        path = 'data/'

        if form.is_valid():
            myfile   = request.FILES['file']

            if myfile.name[-4:] == '.csv' :
                print('SI')
            else:
                messages.error(request, 'Ingresar archivo con formato valido (.csv)')
                return HttpResponseRedirect(reverse('url_patient_upload', args=[patient_id]))

            fs = FileSystemStorage()
            filename = fs.save(path+myfile.name, myfile)
            uploaded_file_url = fs.url(filename)

            new_signal = Signal(name=myfile.name, parameters='')
            new_signal.save()
            new_diagnosis = Diagnosis(doctor=doctor, patient=patient, signal=new_signal, diagnosis='Ingresar diagnostico:...')
            new_diagnosis.save()

            messages.success(request, 'Archivo añadido a la base de datos')
            return HttpResponseRedirect(reverse('url_patient_overview', args=[patient_id]))
        else:
            messages.error(request, 'Ingresar archivo con formato valido')
            return HttpResponseRedirect(reverse('url_patient_view', args=[patient_id]))
    else:
        form = UploadFileForm()

    kwargs = {}
    kwargs['patient']  = patient
    kwargs['title']    = patient.last_name
    kwargs['suptitle'] = patient.first_name
    kwargs['form']     = form
    kwargs['button']   = 'Upload'

    return render(request, 'person/parameters_upload.html', kwargs)
