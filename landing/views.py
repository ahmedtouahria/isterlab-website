from django.shortcuts import render

# Create your views here.


def home(request):

    return render(request, 'pages/home.html')



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

    return render(request, 'pages/coverages.html')



def service_details(request):

    return render(request, 'pages/service_details.html')


def faq(request):

    return render(request, 'pages/faq.html')