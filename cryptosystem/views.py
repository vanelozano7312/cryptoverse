from django.shortcuts import render
from .models import Cryptosystem 
from BackendReady.main import *
from BackendReady.Vigenere import *
from BackendReady.CryptoanalysisVigenere import *
from BackendReady.Hill import *

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
                        if count_falla>=2:
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
                        count_falla=count_falla+1
                        context['countfail']=count_falla
                        context['mistake_decrypt']=True
                    else:
                        if count_falla>=2:
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
                    decode, key_decrypt= decode_mult(codedtext, key_decrypt, count_falla)
                    if decode == -1:
                        count_falla=count_falla+1
                        context['countfail']=count_falla
                        context['mistake_decrypt']=True
                    else:
                        if count_falla>=2:
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
                    encode, key_encrypt = encode_sust(cleartext, key_encrypt, count_falla)
                    if encode == -1:
                        count_falla=count_falla+1
                        context['mistake_encrypt']=True
                        context['countfail']=count_falla
                    else:
                        if count_falla>=2:
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
                    decode, key_decrypt= decode_sust(codedtext, key_decrypt, count_falla)
                    if decode == -1:
                        count_falla=count_falla+1
                        context['countfail']=count_falla
                        context['mistake_decrypt']=True
                    else:
                        if count_falla>=2:
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
                a_key_decrypt = request.POST.get("a_key_decrypt")
                b_key_decrypt = request.POST.get("b_key_decrypt")
                codedtext = request.POST.get("codedtext")
                try:
                    a_key_decrypt=int(a_key_decrypt)
                    b_key_decrypt=int(b_key_decrypt)
                    decode, a_key_decrypt, b_key_decrypt= decode_afin(codedtext, a_key_decrypt, b_key_decrypt, count_falla)
                    print(decode)
                    if decode == -1:
                        count_falla=count_falla+1
                        context['mistake_decrypt']=True
                        if count_falla>2:
                            context['failed_decrypt']=True
                            count_falla=0
                        context['countfail']=count_falla
                    else:
                        if count_falla>2:
                            context['failed_decrypt']=True
                        count_falla=0
                        context['a_key_decrypt']=a_key_decrypt
                        context['b_key_decrypt']=b_key_decrypt
                        context['decrypted']=True
                        context['cleartext']=decode
                        context['encodedtext']=codedtext
                except:
                    pass
                
                
                #ca
                codedtext_ca = request.POST.get("codedtext_ca")
                try:
                    ares, bres, first_two, frecuencies = analisis_afin(codedtext_ca)
                    print(frecuencies)
                    context['frecuencies']=frecuencies
                    context['ares']=ares
                    context['bres']=bres
                    context['first_letter']=first_two[0][0]
                    context['first_frec']=first_two[0][1]
                    context['second_letter']=first_two[1][0]
                    context['second_frec']=first_two[1][1]
                    
                    
                    decode_ca = decode_afin(codedtext_ca, ares, bres, 0)
                    context['cleartext_ca']=decode_ca                        
                    context['encodedtext_ca']=codedtext_ca
                    context['ca']=True
                except:
                    pass

        ##PERMUTATION CYPHER
        elif name == "Permutation":
            view = "permutation.html"
            if request.method == "POST":

                #encrypt
                size_encrypt = request.POST.get("size_encrypt")
                key_encrypt = request.POST.get("key_encrypt")
                cleartext = request.POST.get("cleartext")
                try:
                    size_encrypt=int(size_encrypt)
                    key_encrypt=int(key_encrypt)
                    print(size_encrypt, key_encrypt, cleartext)
                    encode, size_encrypt, key_encrypt = encode_permu(cleartext, size_encrypt, key_encrypt, count_falla)
                    print(encode)
                    if encode == -1:
                        count_falla=count_falla+1
                        context['mistake_encrypt']=True
                        context['countfail']=count_falla
                    else:
                        if count_falla>=2:
                            context['failed_encrypt']=True
                        context['size_encrypt']=size_encrypt
                        context['key_encrypt']=key_encrypt
                        context['encrypted']=True
                        context['cleartext']=cleartext
                        context['encodedtext']=encode
                        count_falla=0
                except:
                    pass

                #decrypt
                size_decrypt = request.POST.get("size_decrypt")
                key_decrypt = request.POST.get("key_decrypt")
                codedtext = request.POST.get("codedtext")
                try:
                    size_decrypt=int(size_decrypt)
                    key_decrypt=int(key_decrypt)
                    decode= decode_permu(codedtext, size_decrypt, key_decrypt, count_falla)
                    if decode == -1:
                        context['mistake_decrypt']=True
                    else:
                        if count_falla==2:
                            context['failed_decrypt']=True
                        count_falla=0
                        context['size_decrypt']=size_decrypt
                        context['key_decrypt']=key_decrypt
                        context['decrypted']=True
                        context['cleartext']=decode
                        context['encodedtext']=codedtext
                except:
                    pass

        ##HILL CYPHER
        elif name == "Hill":
            view = "hill.html"
            if request.method == "POST":
                #encrypt text 
                m_encrypt_text = request.POST.get("m_encrypt_text")
                key_encrypt_text = request.POST.get("key_encrypt_text")
                cleartext_text = request.POST.get("cleartext_text")
                try:
                    m_encrypt_text=int(m_encrypt_text)
                    key_encrypt_text_list = key_encrypt_text.split()
                    print(key_encrypt_text_list)
                    key_encrypt_text_list=strtomat(key_encrypt_text_list, m_encrypt_text)
                    print(key_encrypt_text_list)
                    if key_encrypt_text_list == -1:
                        context['mistake_encrypt_text']=True
                    else:
                        encode_text = encode_hill_text(key_encrypt_text_list, cleartext_text)
                        print(encode_text)

                    if encode_text == -1:
                        context['mistake_encrypt_text']=True
                    else:
                        context['m_encrypt_text']=m_encrypt_text
                        context['key_encrypt_text']=key_encrypt_text_list
                        context['encrypted_text']=True
                        context['cleartext_text']=cleartext_text
                        context['encodedtext_text']=encode_text
                        count_falla=0
                except:
                    pass

                #decrypt text 
                m_decrypt_text = request.POST.get("m_decrypt_text")
                key_decrypt_text = request.POST.get("key_decrypt_text")
                codedtext_text = request.POST.get("codedtext_text")
                try:
                    m_decrypt_text=int(m_decrypt_text)
                    key_decrypt_text_list = key_decrypt_text.split()
                    key_decrypt_text_list=strtomat(key_decrypt_text_list, m_decrypt_text)
                    if key_decrypt_text_list == -1:
                        context['mistake_decrypt_text']=True

                    else:
                        decode_text = decode_hill_text(key_decrypt_text_list, codedtext_text)

                    if decode_text == -1:
                        context['mistake_decrypt_text']=True
                    else:
                        context['m_decrypt_text']=m_decrypt_text
                        context['key_decrypt_text']=key_decrypt_text_list
                        context['decrypted_text']=True
                        context['cleartext_text']=decode_text
                        context['encodedtext_text']=codedtext_text
                except:
                    pass

                
                #encrypt image 
                m_encrypt = request.POST.get("m_encrypt")
                key_encrypt = request.POST.get("key_encrypt")
                url = request.POST.get("url")
                try:
                    m_encrypt=int(m_encrypt)
                    key_encrypt_list = key_encrypt.split()
                    key_encrypt_list=strtomat(key_encrypt_list, m_encrypt)
                    print(key_encrypt_list)
                    if key_encrypt_list == -1:
                        context['mistake_encrypt']=True
                    else:
                        print(key_encrypt_list, url)
                        encode = encode_hill_image(key_encrypt_list, url)
                        print("a")

                    if encode == -1:
                        context['mistake_encrypt']=True
                    else:
                        context['m_encrypt']=m_encrypt
                        context['key_encrypt']=key_encrypt_list
                        context['encrypted']=True
                        count_falla=0
                except:
                    pass

                #decrypt image
                m_decrypt = request.POST.get("m_decrypt")
                key_decrypt = request.POST.get("key_decrypt")
                image = request.POST.get("image")
                print(image)
                try:
                    m_decrypt=int(m_decrypt)
                    key_decrypt_list = key_decrypt.split()
                    key_decrypt_list=strtomat(key_decrypt_list, m_decrypt)
                    if key_decrypt_list == -1:
                        context['mistake_decrypt']=True

                    else:
                        decode = decode_hill_text(key_decrypt_list, codedtext)

                    if decode == -1:
                        context['mistake_decrypt']=True
                    else:
                        context['m_decrypt']=m_decrypt
                        context['key_decrypt']=key_decrypt_list
                        context['decrypted']=True
                        context['cleartext']=decode
                        context['encodedtext']=codedtext
                except:
                    pass

        ##VIGENERE CYPHER
        elif name == "Vigenere":
            view = "vigenere.html"
            if request.method == "POST":

                #encrypt
                key_encrypt = request.POST.get("key_encrypt")
                cleartext = request.POST.get("cleartext")
                try:
                    
                    encode, key_encrypt = encode_vigenere(key_encrypt, cleartext, count_falla)
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
                    decode= decode_vigenere(key_decrypt, codedtext)
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

                #ca
                key_len_ca = request.POST.get("key_len_ca")
                codedtext_ca = request.POST.get("codedtext_ca")
                try:
                    print("a")
                    key_len_ca=int(key_len_ca)
                    print("b")
                    key_len_ca= GuessKeywordLength(key_len_ca, codedtext_ca)
                    print("c")
                    keyword=GuessKeyword(key_len_ca, codedtext_ca)
                    print("d")
                    if keyword == -1:
                        context['mistake_decrypt']=True
                    else:
                        count_falla=0
                        context['keyword']=keyword
                        context['ca']=True
                        decode_ca = decode_vigenere(keyword, codedtext_ca)
                        print("aaaaaa")
                        context['cleartext_ca']=decode_ca
                        context['encodedtext_ca']=codedtext_ca
                except:
                    pass

    return render(request, view, context=context)

