from django.shortcuts import render
from .models import Cryptosystem 
from main import *

# Create your views here.


def cryptosystem_view(request, name=None):
    cryptosystem_obj = None
    view = "cryptosystem.html"
    context = {}
    if name is not None:
        cryptosystem_obj = Cryptosystem.objects.get(name=name)
        context['name']= cryptosystem_obj.name
        context['description']= cryptosystem_obj.description
        encrypted = False
        
        if name == "Shift":
            view = "shift.html"
            if request.method == "POST":
                count_falla = 0
                while not encrypted:
                    key = int(request.POST.get("key"))
                    cleartext = request.POST.get("cleartext")
                    print(key, cleartext)
                    encode = encode_despla(cleartext, key, count_falla)
                    if encode == -1:
                        count_falla=count_falla+1
                    else:
                        encrypted=True
                        context['encrypted']=True
                        print(encode)
                        context['encodedtext']=encode


    return render(request, view, context=context)
