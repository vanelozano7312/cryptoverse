from django.shortcuts import render
from .models import Cryptosystem 
from main import *

# Create your views here.


def cryptosystem_view(request, name=None):
    cryptosystem_obj = None
    view = "cryptosystem.html"
    
    if name is not None:
        cryptosystem_obj = Cryptosystem.objects.get(name=name)
        if name == "Shift":
            view = "shift.html"
            key = request.POST.get("key")
            cleartext = request.POST.get("cleartext")
            print(key, cleartext)


    context = {
        "name" : cryptosystem_obj.name, 
        "description" : cryptosystem_obj.description
    }

    return render(request, view, context=context)
