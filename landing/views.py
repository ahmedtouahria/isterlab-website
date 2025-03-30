from django.shortcuts import render
from .models import *
# Create your views here.


def home(request):
    context = {
        "solutions":Solution.objects.all(),
        "brands":Brand.objects.all(),
    }
    return render(request, 'pages/home.html',context)



def about(request):

    return render(request, 'pages/about.html')



def services(request):

    return render(request, 'pages/services.html')


def project(request):
    return render(request, 'pages/projects.html')


def why_us(request):

    return render(request, 'pages/why_us.html')


def contact(request):

    return render(request, 'pages/contact.html')


def coverages(request):

    context = {
        "coverages": Coverage.objects.all()
    }

    return render(request, 'pages/coverages.html',context)



def service_details(request,name):
    context = {
        "service": Service.objects.get(name=name)
    }
    return render(request, 'pages/service_details.html',context)

def solution_details(request,name):
    context = {
        "solution":Solution.objects.get(name=name)
    }
    return render(request, 'pages/solution_details.html',context)

def faq(request):

    return render(request, 'pages/faq.html')


def become_a_partner(request):

    return render(request, 'pages/become_a_partner.html')