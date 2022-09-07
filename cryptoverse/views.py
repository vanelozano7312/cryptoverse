from django.http import HttpResponse 
from django.template.loader import render_to_string
from cryptosystem.models import Cryptosystem


def home_view(request, *args, **kwargs):

    cryptosystem_qs = Cryptosystem.objects.all()

    context = {
        "object_list" : cryptosystem_qs,
    }

    HTML_STRING = render_to_string("home_view.html", context=context)
   
    return HttpResponse(HTML_STRING)