from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def index(request):
    #return HttpResponse("Hello, world. You're at the polls index.")
    return HttpResponseRedirect(reverse('url_home'))


def home(request):
    kwargs = {'title': 'Holter Monitor Web'}
    kwargs['no_sidebar'] = True
    kwargs['title']      = '¡Bienvenido!'
    kwargs['suptitle']   = ''
    return render(request, 'main/body.html', kwargs)
