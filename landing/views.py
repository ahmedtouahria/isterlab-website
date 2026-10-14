import json
from django.shortcuts import get_object_or_404, redirect, render
import requests
from .models import *
from constance import config
def verify_recaptcha(token):
    if not token or not config.RECAPTCHA_SECRET_KEY:
        return False
    try:
        response = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={'secret': config.RECAPTCHA_SECRET_KEY, 'response': token},
            timeout=10,
        )
        response.raise_for_status()
        return response.json().get('success') is True
    except (requests.RequestException, ValueError, AttributeError):
        return False



def home(request):
    context = {
        "solutions":Solution.objects.all(),
        "brands":Brand.objects.all(),
    }
    return render(request, 'pages/home.html',context)



def about(request):

    return render(request, 'pages/about.html')



def services(request):

    context = {
        "services": Service.objects.all(),
    }

    return render(request, 'pages/services.html',context)

def solutions(request):
    context = {
        "solutions":Solution.objects.all(),
    }
    return render(request, 'pages/solutions.html',context)


def project(request):
    return render(request, 'pages/projects.html')


def why_us(request):
    context = {
        "brands":Brand.objects.all(),
        
    }
    return render(request, 'pages/why_us.html',context)


def contact(request):
    if request.method == 'POST':
        con_name = request.POST.get('con_name')
        con_email = request.POST.get('con_email')
        con_subject = request.POST.get('con_subject')
        con_message = request.POST.get('con_message')
        recaptcha_response = request.POST.get('g-recaptcha-response')

         # Verify reCAPTCHA
        if verify_recaptcha(recaptcha_response):

            contact_obj,_ = Contact.objects.get_or_create(
                name = con_name,
                email = con_email,
                subject = con_subject,
                message = con_message
            )
            # reCAPTCHA passed, process the form (e.g., send email, save to DB)
            return render(request, 'pages/contact.html', {"message": "Your message has been sent successfully!"})
        else:
            # reCAPTCHA failed
            return render(request, 'pages/contact.html', {"error": "reCAPTCHA verification failed. Please try again."})

    coverages = list(Coverage.objects.values("name", "latitude", "longitude"))
    
    context = {
        "coverages_json": json.dumps(coverages)  # Convert to JSON for JavaScript
    }
    
    return render(request, 'pages/contact.html',context)


def coverages(request):
    coverages = list(Coverage.objects.values("name", "latitude", "longitude"))
    
    context = {
        "coverages_json": json.dumps(coverages)  # Convert to JSON for JavaScript
    }
    
    return render(request, 'pages/coverages.html', context)


def service_details(request,name):
    context = {
        "service": get_object_or_404(Service, name=name)
    }
    return render(request, 'pages/service_details.html',context)

def solution_details(request,name):
    context = {
        "solution":get_object_or_404(Solution, name=name)
    }
    return render(request, 'pages/solution_details.html',context)

def faq(request):
    context = {
        "faqs":FAQ.objects.all()
    }
    return render(request, 'pages/faq.html',context)


def become_a_partner(request):
    if request.method == 'POST':
        con_name = request.POST.get('con_name')
        con_email = request.POST.get('con_email')
        con_subject = request.POST.get('con_subject')
        con_company = request.POST.get('company_name')
        con_company_url = request.POST.get('company_url')
        con_country = request.POST.get('con_country')
        con_state = request.POST.get('con_state')
        cv = request.FILES.get('con_cv')

        con_message = request.POST.get('con_message')
        recaptcha_response = request.POST.get('g-recaptcha-response')

         # Verify reCAPTCHA
        if verify_recaptcha(recaptcha_response):

            contact_obj,_ = ContactPartner.objects.get_or_create(
                name = con_name,
                email = con_email,
                subject = con_subject,
                message = con_message,
                company=con_company,
                company_url = con_company_url,
                country = con_country,
                state = con_state,
                cv=cv
            )
            # reCAPTCHA passed, process the form (e.g., send email, save to DB)
            return render(request, 'pages/become_a_partner.html', {"message": "Your message has been sent successfully!"})
        else:
            # reCAPTCHA failed
            return render(request, 'pages/become_a_partner.html', {"error": "reCAPTCHA verification failed. Please try again."})

    return render(request, 'pages/become_a_partner.html')


def blogs(request):

    context = {
        "blogs":Blog.objects.all()
    }
    return render(request, 'pages/blogs.html',context)


def blog_details(request,slug):

    context = {
    "blog":get_object_or_404(Blog, slug=slug)
    }

    return render(request, 'pages/blog_details.html',context)
def privacy_terms(request):

    return render(request, 'pages/terms_policy.html')