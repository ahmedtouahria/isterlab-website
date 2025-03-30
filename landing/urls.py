from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name="home"),
    path("about/",about,name="about"),
    path("services/",services,name="services"),
    path("projects/",project,name="projects"),
    path("why_choose_isterlab/",why_us,name="why_us"),
    path("contact/",contact,name="contact"),
    path("become-a-partner/",become_a_partner,name="become_a_partner"),

    path("coverages/",coverages,name="coverages"),
    path("service_details/<str:name>/",service_details,name="service_details"),
    path("solutions/<str:name>/",solution_details,name="solution_details"),

    path("faq/",faq,name="faq"),


]
