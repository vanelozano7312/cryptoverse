from django.http import HttpResponse 
from django.template.loader import render_to_string
from cryptosystem.models import Cryptosystem
from cryptosystem.views import *


def home_view(request, *args, **kwargs):

    cryptosystem_qs = Cryptosystem.objects.all()
    change_page("home")

    context = {
        "object_list" : cryptosystem_qs,
    }

    HTML_STRING = render_to_string("home_view.html", context=context)
   
    return HttpResponse(HTML_STRING)

def classic_view(request, *args, **kwargs):

    cryptosystem_qs = Cryptosystem.objects.all()
    change_page("home")

    context = {
        "object_list" : cryptosystem_qs,
    }

    HTML_STRING = render_to_string("classic.html", context=context)
   
    return HttpResponse(HTML_STRING)

def block_view(request, *args, **kwargs):

    cryptosystem_qs = Cryptosystem.objects.all()
    change_page("home")

    context = {
        "object_list" : cryptosystem_qs,
    }

    HTML_STRING = render_to_string("block.html", context=context)
   
    return HttpResponse(HTML_STRING)