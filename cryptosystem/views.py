from django.shortcuts import render
from .models import Cryptosystem 
from main import *
# Create your views here.

count_falla=0
encrypted = False
page=''

def change_page(name):
    global page
    global count_falla
    global encrypted
    if name!= page:
        page=name
        count_falla=0
        encrypted =False



def cryptosystem_view(request, name=None):
    cryptosystem_obj = None
    view = "cryptosystem.html"
    context = {}
    global count_falla
    encrypted=False

    if name is not None:
        cryptosystem_obj = Cryptosystem.objects.get(name=name)
        change_page(cryptosystem_obj.name)
        context['name']= cryptosystem_obj.name
        context['description']= cryptosystem_obj.description
        
        if name == "Shift":
            view = "shift.html"
            if request.method == "POST":
                if not encrypted:
                    key = request.POST.get("key")
                    cleartext = request.POST.get("cleartext")
                    print(key, cleartext, count_falla)
                    try:
                        key=int(key)
                        encode, key = encode_despla(cleartext, key, count_falla)
                        if encode == -1:
                            count_falla=count_falla+1
                            context['mistake']=True
                            context['countfail']=count_falla
                        else:
                            encrypted=True
                            count_falla=0
                            context['key']=key
                            context['encrypted']=True
                            context['cleartext']=cleartext
                            context['encodedtext']=encode
                    except:
                        pass
                # if encrypted:
                #     encrypt_again = request.POST.get("encrypt_again")
                #     if encrypt_again == "Encrypt":
                #         count_falla=0
                #         context={}
                #         context['encrypted']=False
                #         context['mistake']=False
                #         encrypt_again = "not"

    return render(request, view, context=context)
