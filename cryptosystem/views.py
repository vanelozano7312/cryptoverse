from django.shortcuts import render
from .models import Cryptosystem 
from main import *

#Global variables and function to count the user mistakes and restart 
#that count every time the user goes into another page

count_falla=0
page=''

def change_page(name):
    global page
    global count_falla
    if name!= page:
        page=name
        count_falla=0

#views for every cryptosystem
def cryptosystem_view(request, name=None):
    cryptosystem_obj = None
    view = "cryptosystem.html"
    context = {}
    global count_falla

    if name is not None:
        cryptosystem_obj = Cryptosystem.objects.get(name=name)
        change_page(cryptosystem_obj.name)
        context['name']= cryptosystem_obj.name
        context['description']= cryptosystem_obj.description
        
        ##SHIFT CYPHER
        if name == "Shift":
            view = "shift.html"
            if request.method == "POST":

                #encrypt
                key_encrypt = request.POST.get("key_encrypt")
                cleartext = request.POST.get("cleartext")
                try:
                    key_encrypt=int(key_encrypt)
                    encode, key_encrypt = encode_despla(cleartext, key_encrypt, count_falla)
                    if encode == -1:
                        count_falla=count_falla+1
                        context['mistake_encrypt']=True
                        context['countfail']=count_falla
                    else:
                        if count_falla==2:
                            context['failed_encrypt']=True
                        context['key_encrypt']=key_encrypt
                        context['encrypted']=True
                        context['cleartext']=cleartext
                        context['encodedtext']=encode
                        count_falla=0
                except:
                    pass

                #decrypt
                key_decrypt = request.POST.get("key_decrypt")
                codedtext = request.POST.get("codedtext")
                try:
                    key_decrypt=int(key_decrypt)
                    decode= decode_despla(codedtext, key_decrypt, count_falla)
                    print(decode)
                    if decode == -1:
                        context['mistake_decrypt']=True
                    else:
                        if count_falla==2:
                            context['failed_decrypt']=True
                        count_falla=0
                        context['key_decrypt']=key_decrypt
                        context['decrypted']=True
                        context['cleartext']=decode
                        context['encodedtext']=codedtext
                except:
                    pass

        ##MULTIPLICATION CYPHER
        elif name == "Multiplication":
            view = "multiplication.html"
            if request.method == "POST":
                #encrypt
                key_encrypt = request.POST.get("key_encrypt")
                cleartext = request.POST.get("cleartext")
                try:
                    key_encrypt=int(key_encrypt)
                    encode, key_encrypt = encode_mult(cleartext, key_encrypt, count_falla)
                    if encode == -1:
                        count_falla=count_falla+1
                        context['mistake_encrypt']=True
                        context['countfail']=count_falla
                    else:
                        if count_falla==2:
                            context['failed_encrypt']=True
                        context['key_encrypt']=key_encrypt
                        context['encrypted']=True
                        context['cleartext']=cleartext
                        context['encodedtext']=encode
                        count_falla=0
                except:
                    pass

                #decrypt
                key_decrypt = request.POST.get("key_decrypt")
                codedtext = request.POST.get("codedtext")
                try:
                    key_decrypt=int(key_decrypt)
                    decode= decode_mult(codedtext, key_decrypt, count_falla)
                    print(decode)
                    if decode == -1:
                        context['mistake_decrypt']=True
                    else:
                        if count_falla==2:
                            context['failed_decrypt']=True
                        count_falla=0
                        context['key_decrypt']=key_decrypt
                        context['decrypted']=True
                        context['cleartext']=decode
                        context['encodedtext']=codedtext
                except:
                    pass
            
        ##SUBSTITUTIION CYPHER
        elif name == "Substitution":
            view = "substitution.html"
            if request.method == "POST":
                #encrypt
                key_encrypt = request.POST.get("key_encrypt")
                cleartext = request.POST.get("cleartext")
                try:
                    key_encrypt=int(key_encrypt)
                    encode, key_encrypt = encode_mult(cleartext, key_encrypt, count_falla)
                    if encode == -1:
                        count_falla=count_falla+1
                        context['mistake_encrypt']=True
                        context['countfail']=count_falla
                    else:
                        if count_falla==2:
                            context['failed_encrypt']=True
                        context['key_encrypt']=key_encrypt
                        context['encrypted']=True
                        context['cleartext']=cleartext
                        context['encodedtext']=encode
                        count_falla=0
                except:
                    pass

                #decrypt
                key_decrypt = request.POST.get("key_decrypt")
                codedtext = request.POST.get("codedtext")
                try:
                    key_decrypt=int(key_decrypt)
                    decode= decode_mult(codedtext, key_decrypt, count_falla)
                    print(decode)
                    if decode == -1:
                        context['mistake_decrypt']=True
                    else:
                        if count_falla==2:
                            context['failed_decrypt']=True
                        count_falla=0
                        context['key_decrypt']=key_decrypt
                        context['decrypted']=True
                        context['cleartext']=decode
                        context['encodedtext']=codedtext
                except:
                    pass

        ##AFFINE CYPHER
        elif name == "Affine":
            view = "affine.html"
            if request.method == "POST":

                #encrypt
                a_key_encrypt = request.POST.get("a_key_encrypt")
                b_key_encrypt = request.POST.get("b_key_encrypt")
                cleartext = request.POST.get("cleartext")
                try:
                    a_key_encrypt=int(a_key_encrypt)
                    b_key_encrypt=int(b_key_encrypt)
                    encode, a_key_encrypt, b_key_encrypt = encode_afin(cleartext, a_key_encrypt, b_key_encrypt, count_falla)
                    if encode == -1:
                        count_falla=count_falla+1
                        context['mistake_encrypt']=True
                        context['countfail']=count_falla
                    else:
                        if count_falla==2:
                            context['failed_encrypt']=True
                        context['a_key_encrypt']=a_key_encrypt
                        context['b_key_encrypt']=b_key_encrypt
                        context['encrypted']=True
                        context['cleartext']=cleartext
                        context['encodedtext']=encode
                        count_falla=0
                except:
                    pass

                #decrypt
                a_key_encrypt = request.POST.get("a_key_encrypt")
                b_key_encrypt = request.POST.get("b_key_encrypt")
                codedtext = request.POST.get("codedtext")
                try:
                    a_key_encrypt=int(a_key_encrypt)
                    b_key_encrypt=int(b_key_encrypt)
                    decode= decode_despla(codedtext, key_decrypt, count_falla)
                    if decode == -1:
                        context['mistake_decrypt']=True
                    else:
                        if count_falla==2:
                            context['failed_decrypt']=True
                        count_falla=0
                        context['a_key_encrypt']=a_key_encrypt
                        context['b_key_encrypt']=b_key_encrypt
                        context['decrypted']=True
                        context['cleartext']=decode
                        context['encodedtext']=codedtext
                except:
                    pass

        ##PERMUTATION CYPHER
        elif name == "Permutation":
            view = "permutation.html"
        ##HILL CYPHER
        elif name == "Hill":
            view = "hill.html"
        ##VIGENERE CYPHER
        elif name == "Vigenere":
            view = "vigenere.html"


    return render(request, view, context=context)

