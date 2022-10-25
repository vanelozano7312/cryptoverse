from turtle import clear
import string
from django.shortcuts import render
from .models import Cryptosystem 
from BackendReady.main import *
from BackendReady.Vigenere import *
from BackendReady.CryptoanalysisVigenere import *
from BackendReady.CryptoanalysisHill import *
from BackendReady.Hill import *
from BackendReady.SDES import *
from BackendReady.TDES import *
from BackendReady.AES import *
from BackendReady.GammaPentagonal import *
import codecs
# from .forms import HillImageForm
from django.core.files.storage import FileSystemStorage

import os
import sys
import mimetypes
import time
#Global variables and function to count the user mistakes and restart 
#that count every time the user goes into another page

count_falla=0
page=''
permutacion = "0 1 2 3 4 5 6 7 8 9"
punto_inicial_x = 0
punto_inicial_y = 0
vectores = {}

def change_page(name):
    global page
    global count_falla
    if name!= page:
        page=name
        count_falla=0
        default_graph()

def default_graph():
    global permutacion   
    permutacion = "0 1 2 3 4 5 6 7 8 9"
    permutacion = convertirPermutacion(permutacion)
    global punto_inicial_x
    global punto_inicial_y
    punto_inicial_x, punto_inicial_y = 0, 0
    nuevoGrafo(0, 0, permutacion)


#views for every cryptosystem
def cryptosystem_view(request, name=None):
    cryptosystem_obj = None
    view = "cryptosystem.html"
    context = {}
    global count_falla
    global permutacion
    global punto_inicial_x
    global punto_inicial_y
    global vectores

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
                    context['frecuencies']=frecuencies
                    context['ares']=ares
                    context['bres']=bres
                    context['first_letter']=first_two[0][0]
                    context['first_frec']=first_two[0][1]
                    context['second_letter']=first_two[1][0]
                    context['second_frec']=first_two[1][1]
                    
                    
                    decode_ca, a, b = decode_afin(codedtext_ca, ares, bres, 0)
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
                    encode, size_encrypt, key_encrypt = encode_permu(cleartext, size_encrypt, key_encrypt, count_falla)
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
                    decode = decode_permu(codedtext, size_decrypt, key_decrypt, count_falla)
                    if decode == -1:
                        context['mistake_decrypt']=True
                    else:
                        if count_falla==2:
                            context['failed_decrypt']=True
                        count_falla=0
                        context['size_decrypt']=decode[1]
                        context['key_decrypt']=decode[2]
                        context['decrypted']=True
                        context['cleartext']=decode[0]
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
                    key_encrypt_text_list=strtomat(key_encrypt_text_list, m_encrypt_text)
                    if key_encrypt_text_list == -1:
                        context['mistake_encrypt_text']=True
                    else:
                        encode_text= encode_hill_text(key_encrypt_text_list, cleartext_text)

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
                    if key_encrypt_list == -1:
                        context['mistake_encrypt']=True
                    else:
                        encode = encode_hill_image(key_encrypt_list, url)
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
                
                if 'Decryptimage' in request.POST:
                    m_decrypt = request.POST.get("m_decrypt")
                    key_decrypt = request.POST.get("key_decrypt")
                    if os.path.exists("static/images/clean.png"):
                        os.remove("static/images/clean.png")
                    upload = request.FILES.get("im1")
                    fss = FileSystemStorage()
                    fss.save('static/images/clean.png', upload)
                    try:
                        m_decrypt=int(m_decrypt)
                        key_decrypt_list = key_decrypt.split()
                        key_decrypt_list=strtomat(key_decrypt_list, m_decrypt)
                        if key_decrypt_list == -1:
                            context['mistake_decrypt']=True
                        else:
                            decode = decode_hill_image(key_decrypt_list, 'static/images/clean.png')

                        if decode == -1:
                            context['mistake_decrypt']=True
                        else:
                            context['m_decrypt']=m_decrypt
                            context['key_decrypt']=key_decrypt_list
                            context['decrypted']=True
                    except:
                        pass
                    
                #cryptoanalisis
                
                if 'Cryptoanalisis' in request.POST:
                    m_ca = request.POST.get("m_ca")
                    x = request.POST.get("x")
                    y = request.POST.get("y")
                    n = request.POST.get("n")
                    try:
                        m_ca=int(m_ca)
                        n=int(n)
                        x_list = x.split()
                        x_list=strtomat(x_list, m_ca)
                        y_list = y.split()
                        y_list=strtomat(y_list, m_ca)
                        if x_list == -1 or y_list == -1:
                            context['mistake_decrypt']=True
                        else:
                            key = ca_hill(x_list, y_list, n)

                        if key.any() == -1:
                            context['mistake_ca']=True
                            context['x']=x
                            context['y']=y
                            context['n']=n
                        else:
                            context['ca']=True
                            context['m_ca']=m_ca
                            context['x']=x_list
                            context['y']=y_list
                            context['n']=n
                            context['key']=key
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
                    key_len_ca=int(key_len_ca)
                    key_len_ca= GuessKeywordLength(key_len_ca, codedtext_ca)
                    keyword=GuessKeyword(key_len_ca, codedtext_ca)
                    if keyword == -1:
                        context['mistake_decrypt']=True
                    else:
                        count_falla=0
                        context['keyword']=keyword
                        context['ca']=True
                        decode_ca = decode_vigenere(keyword, codedtext_ca)
                        context['cleartext_ca']=decode_ca
                        context['encodedtext_ca']=codedtext_ca
                except:
                    pass
        
        ##SDES CYPHER
        elif name == "SDES":
            view = "s-des.html"
            if request.method == "POST":
                    
                #encrypt
                encrypt = request.POST.get("encrypt")
                if encrypt == "Encrypt":
                    key_encrypt_text = request.POST.get("key_encrypt")
                    cleartext_text = request.POST.get("cleartext")
                    error = False
                    try:
                        try:
                            allowed = set('0'+'1'+' ')
                            if set(key_encrypt_text) > allowed:
                                error = True
                            if set(cleartext_text) > allowed:
                                error = True
                            key_encrypt_text_list = key_encrypt_text.split()
                            key_encrypt_text_list = [int(x) for x in key_encrypt_text_list]
                            if len(key_encrypt_text_list) != 10:
                                error = True

                            cleartext = cleartext_text.split()
                            cleartext = [int(x) for x in cleartext]
                            keys = generate_keys_sdes(key_encrypt_text_list)
                            encode_text= encode_sdes_text(cleartext, keys)
                        except:
                            encode_text=-1
                        if encode_text == -1 or error:
                            count_falla=count_falla+1
                            if count_falla>=3:
                                context['failed_encrypt']=True
                                context['key']=randomkey()
                                count_falla=0
                            else:
                                context['mistake_encrypt']=True
                                context['countfail']=count_falla
                        else:
                            context['encrypted']=True
                            context['cleartext']=cleartext_text
                            encode_text = [str(x) for x in encode_text]
                            context['encodedtext']=' '.join(encode_text)
                            count_falla=0
                    except:
                        pass


                #decrypt
                decrypt = request.POST.get("decrypt")
                if decrypt == "Decrypt":
                    key_decrypt_text = request.POST.get("key_decrypt")
                    codedtext_text = request.POST.get("codedtext")
                    error = False
                    try:
                        try:
                            allowed = {'0', '1', ' '}

                            for i in key_decrypt_text:
                                if i not in allowed:
                                    error = True
                            
                            for i in codedtext_text:
                                if i not in allowed:
                                    error = True

                            key_decrypt_text_list = key_decrypt_text.split()
                            key_decrypt_text_list = [int(x) for x in key_decrypt_text_list]
                            if len(key_decrypt_text_list) != 10:
                                error = True

                            codedtext = codedtext_text.split()
                            codedtext = [int(x) for x in codedtext]
                            keys = generate_keys_sdes(key_decrypt_text_list)
                            decode_text = decode_sdes_text(codedtext, keys)
                        except:
                            decode_text = -1
                            
                        if decode_text == -1 or error:
                            count_falla=count_falla+1
                            # if count_falla>=3:
                            #     context['failed_encrypt']=True
                            #     count_falla=0
                            # else:
                            context['countfail']=count_falla
                            context['mistake_decrypt']=True
                        else:
                            key_decrypt_text_list = [str(x) for x in key_decrypt_text_list]
                            context['key_decrypt']=' '.join(key_decrypt_text_list)
                            context['decrypted']=True
                            decode_text = [str(x) for x in decode_text]
                            context['cleartext']=' '.join(decode_text)
                            context['encodedtext']=codedtext_text
                            count_falla=0
                    except:
                        pass
        
        ##T-DES CYPHER
        elif name == "TDES":
            view = "t-des.html"
            if request.method == "POST":
                
                #encrypt in ECB MODE
                if 'Encrypt_ECB' in request.POST:
                    key_encrypt1 = request.POST.get("key_encrypt_1")
                    key_encrypt2 = request.POST.get("key_encrypt_2")
                    key_encrypt3 = request.POST.get("key_encrypt_3")

                    url = request.POST.get("url")
                    try:
                        key_encrypt1 = key_encrypt1.upper()
                        key_encrypt2 = key_encrypt2.upper()
                        key_encrypt3 = key_encrypt3.upper()
                        encode = encode_tdes_image_ecb(key_encrypt1, key_encrypt2, key_encrypt3, url)
                        if encode == -1:
                            count_falla=count_falla+1
                            if count_falla>=3:
                                print("ya estoy creando uno nuevo")
                                key_encrypt1 = randomkeyhexa()
                                key_encrypt2 = randomkeyhexa()
                                key_encrypt3 = randomkeyhexa()
                                context['failed_encrypt_ecb']=True
                                context['key_encrypt_1'] = key_encrypt1
                                context['key_encrypt_2'] = key_encrypt2
                                context['key_encrypt_3'] = key_encrypt3
                                encode = encode_tdes_image_ecb(key_encrypt1, key_encrypt2, key_encrypt3, url)
                                context['encrypted_ecb']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_ecb']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt_1'] = key_encrypt1
                            context['key_encrypt_2'] = key_encrypt2
                            context['key_encrypt_3'] = key_encrypt3
                            context['encrypted_ecb']=True
                            count_falla=0
                    except:
                        pass
                
                #decrypt in ECB MODE
                if 'Decrypt_ECB' in request.POST:
                    try:
                        try:
                            key_decrypt_1 = request.POST.get("key_decrypt_1")
                            key_decrypt_2 = request.POST.get("key_decrypt_2")
                            key_decrypt_3 = request.POST.get("key_decrypt_3")
                            
                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt_1 = key_decrypt_1.upper()
                            key_decrypt_2 = key_decrypt_2.upper()
                            key_decrypt_3 = key_decrypt_3.upper()
                            decode = decode_tdes_image_ecb(key_decrypt_1, key_decrypt_2, key_decrypt_3, 'static/images/clean.png')
                        except:
                            decode= -1
                        if decode == -1:
                            context['mistake_decrypt_ecb']=True
                        else:
                            context['key_decrypt_1']=key_decrypt_1
                            context['key_decrypt_2']=key_decrypt_2
                            context['key_decrypt_3']=key_decrypt_3
                            context['decrypted_ecb']=True
                    except:
                        pass
                
                #encrypt in CBC MODE
                if 'Encrypt_CBC' in request.POST:
                    key_encrypt1 = request.POST.get("key_encrypt_1")
                    key_encrypt2 = request.POST.get("key_encrypt_2")
                    key_encrypt3 = request.POST.get("key_encrypt_3")
                    iv_encrypt = request.POST.get("iv_encrypt")

                    url = request.POST.get("url")
                    try:
                        try:
                            key_encrypt1 = key_encrypt1.upper()
                            key_encrypt2 = key_encrypt2.upper()
                            key_encrypt3 = key_encrypt3.upper()
                            iv_encrypt = iv_encrypt.upper()
                            encode = encode_tdes_image_cbc(key_encrypt1, key_encrypt2, key_encrypt3, iv_encrypt, url)
                        except:
                            encode=-1
                        if encode == -1:
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt1 = randomkeyhexa()
                                key_encrypt2 = randomkeyhexa()
                                key_encrypt3 = randomkeyhexa()
                                iv_encrypt = randomkeyhexa()
                                context['failed_encrypt_cbc']=True
                                context['key_encrypt_1'] = key_encrypt1
                                context['key_encrypt_2'] = key_encrypt2
                                context['key_encrypt_3'] = key_encrypt3
                                context['iv_encrypt'] = iv_encrypt
                                encode = encode_tdes_image_cbc(key_encrypt1, key_encrypt2, key_encrypt3, iv_encrypt, url)
                                context['encrypted_cbc']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_cbc']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt_1'] = key_encrypt1
                            context['key_encrypt_2'] = key_encrypt2
                            context['key_encrypt_3'] = key_encrypt3
                            context['iv_encrypt'] = iv_encrypt
                            context['encrypted_cbc']=True
                            count_falla=0
                    except:
                        pass

                
                #decrypt in CBC MODE
                if 'Decrypt_CBC' in request.POST:
                    try:
                        try:
                            key_decrypt_1 = request.POST.get("key_decrypt_1")
                            key_decrypt_2 = request.POST.get("key_decrypt_2")
                            key_decrypt_3 = request.POST.get("key_decrypt_3")
                            iv_decrypt = request.POST.get("iv_decrypt")

                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt_1 = key_decrypt_1.upper()
                            key_decrypt_2 = key_decrypt_2.upper()
                            key_decrypt_3 = key_decrypt_3.upper()
                            iv_decrypt = iv_decrypt.upper()
                            decode = decode_tdes_image_cbc(key_decrypt_1, key_decrypt_2, key_decrypt_3, iv_decrypt, 'static/images/clean.png')
                        except:
                            decode=-1
                        if decode == -1:
                            context['mistake_decrypt_cbc']=True
                        else:
                            context['key_decrypt_1']=key_decrypt_1
                            context['key_decrypt_2']=key_decrypt_2
                            context['key_decrypt_3']=key_decrypt_3
                            context['iv_decrypt']=iv_decrypt
                            context['decrypted_cbc']=True
                    except:
                        pass
                
                #encrypt in OFB MODE
                if 'Encrypt_OFB' in request.POST:
                    key_encrypt1 = request.POST.get("key_encrypt_1")
                    key_encrypt2 = request.POST.get("key_encrypt_2")
                    key_encrypt3 = request.POST.get("key_encrypt_3")
                    iv_encrypt = request.POST.get("iv_encrypt")

                    url = request.POST.get("url")
                    try:
                        try:
                            key_encrypt1 = key_encrypt1.upper()
                            key_encrypt2 = key_encrypt2.upper()
                            key_encrypt3 = key_encrypt3.upper()
                            iv_encrypt = iv_encrypt.upper()
                            encode = encode_tdes_image_ofb(key_encrypt1, key_encrypt2, key_encrypt3, iv_encrypt, url)
                        except:
                            encode=-1
                        if encode == -1:
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt1 = randomkeyhexa()
                                key_encrypt2 = randomkeyhexa()
                                key_encrypt3 = randomkeyhexa()
                                iv_encrypt = randomkeyhexa()
                                context['failed_encrypt_ofb']=True
                                context['key_encrypt_1'] = key_encrypt1
                                context['key_encrypt_2'] = key_encrypt2
                                context['key_encrypt_3'] = key_encrypt3
                                context['iv_encrypt'] = iv_encrypt
                                encode = encode_tdes_image_ofb(key_encrypt1, key_encrypt2, key_encrypt3, iv_encrypt, url)
                                context['encrypted_ofb']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_ofb']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt_1'] = key_encrypt1
                            context['key_encrypt_2'] = key_encrypt2
                            context['key_encrypt_3'] = key_encrypt3
                            context['iv_encrypt'] = iv_encrypt
                            context['encrypted_ofb']=True
                            count_falla=0
                    except:
                        pass

                
                #decrypt in OFB MODE
                if 'Decrypt_OFB' in request.POST:
                    try:
                        try:
                            key_decrypt_1 = request.POST.get("key_decrypt_1")
                            key_decrypt_2 = request.POST.get("key_decrypt_2")
                            key_decrypt_3 = request.POST.get("key_decrypt_3")
                            iv_decrypt = request.POST.get("iv_decrypt")

                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt_1 = key_decrypt_1.upper()
                            key_decrypt_2 = key_decrypt_2.upper()
                            key_decrypt_3 = key_decrypt_3.upper()
                            iv_decrypt = iv_decrypt.upper()
                            decode = decode_tdes_image_ofb(key_decrypt_1, key_decrypt_2, key_decrypt_3, iv_decrypt, 'static/images/clean.png')
                        except:
                            decode=-1
                        if decode == -1:
                            context['mistake_decrypt_ofb']=True
                        else:
                            context['key_decrypt_1']=key_decrypt_1
                            context['key_decrypt_2']=key_decrypt_2
                            context['key_decrypt_3']=key_decrypt_3
                            context['iv_decrypt']=iv_decrypt
                            context['decrypted_ofb']=True
                    except:
                        pass
                
                #encrypt in CFB MODE
                if 'Encrypt_CFB' in request.POST:
                    key_encrypt1 = request.POST.get("key_encrypt_1")
                    key_encrypt2 = request.POST.get("key_encrypt_2")
                    key_encrypt3 = request.POST.get("key_encrypt_3")
                    iv_encrypt = request.POST.get("iv_encrypt")

                    url = request.POST.get("url")
                    try:
                        try:
                            key_encrypt1 = key_encrypt1.upper()
                            key_encrypt2 = key_encrypt2.upper()
                            key_encrypt3 = key_encrypt3.upper()
                            iv_encrypt = iv_encrypt.upper()
                            encode = encode_tdes_image_cfb(key_encrypt1, key_encrypt2, key_encrypt3, iv_encrypt, url)
                        except:
                            encode=-1
                        if encode == -1:
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt1 = randomkeyhexa()
                                key_encrypt2 = randomkeyhexa()
                                key_encrypt3 = randomkeyhexa()
                                iv_encrypt = randomkeyhexa()
                                context['failed_encrypt_cfb']=True
                                context['key_encrypt_1'] = key_encrypt1
                                context['key_encrypt_2'] = key_encrypt2
                                context['key_encrypt_3'] = key_encrypt3
                                context['iv_encrypt'] = iv_encrypt
                                encode = encode_tdes_image_cfb(key_encrypt1, key_encrypt2, key_encrypt3, iv_encrypt, url)
                                context['encrypted_cfb']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_cfb']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt_1'] = key_encrypt1
                            context['key_encrypt_2'] = key_encrypt2
                            context['key_encrypt_3'] = key_encrypt3
                            context['iv_encrypt'] = iv_encrypt
                            context['encrypted_cfb']=True
                            count_falla=0
                    except:
                        pass
                
                #decrypt in CFB MODE
                if 'Decrypt_CFB' in request.POST:
                    try:
                        try:
                            key_decrypt_1 = request.POST.get("key_decrypt_1")
                            key_decrypt_2 = request.POST.get("key_decrypt_2")
                            key_decrypt_3 = request.POST.get("key_decrypt_3")
                            iv_decrypt = request.POST.get("iv_decrypt")

                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt_1 = key_decrypt_1.upper()
                            key_decrypt_2 = key_decrypt_2.upper()
                            key_decrypt_3 = key_decrypt_3.upper()
                            iv_decrypt = iv_decrypt.upper()
                            decode = decode_tdes_image_cfb(key_decrypt_1, key_decrypt_2, key_decrypt_3, iv_decrypt, 'static/images/clean.png')
                        except:
                            decode=-1
                        if decode == -1:
                            context['mistake_decrypt_cfb']=True
                        else:
                            context['key_decrypt_1']=key_decrypt_1
                            context['key_decrypt_2']=key_decrypt_2
                            context['key_decrypt_3']=key_decrypt_3
                            context['iv_decrypt']=iv_decrypt
                            context['decrypted_cfb']=True
                    except:
                        pass
                
                #encrypt in CTR MODE
                if 'Encrypt_CTR' in request.POST:
                    key_encrypt1 = request.POST.get("key_encrypt_1")
                    key_encrypt2 = request.POST.get("key_encrypt_2")
                    key_encrypt3 = request.POST.get("key_encrypt_3")
                    ctr_encrypt = request.POST.get("ctr_encrypt")

                    url = request.POST.get("url")
                    
                    try:
                        try:
                            key_encrypt1 = key_encrypt1.upper()
                            key_encrypt2 = key_encrypt2.upper()
                            key_encrypt3 = key_encrypt3.upper()
                            ctr_encrypt = ctr_encrypt.upper()
                            encode = encode_tdes_image_ctr(key_encrypt1, key_encrypt2, key_encrypt3, ctr_encrypt, url)
                        except:
                            encode=-1
                        if encode == -1:
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt1 = randomkeyhexa()
                                key_encrypt2 = randomkeyhexa()
                                key_encrypt3 = randomkeyhexa()
                                ctr_encrypt = randomkeyhexa()
                                context['failed_encrypt_ctr']=True
                                context['key_encrypt_1'] = key_encrypt1
                                context['key_encrypt_2'] = key_encrypt2
                                context['key_encrypt_3'] = key_encrypt3
                                context['ctr_encrypt'] = ctr_encrypt
                                encode = encode_tdes_image_ctr(key_encrypt1, key_encrypt2, key_encrypt3, ctr_encrypt, url)
                                context['encrypted_ctr']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_ctr']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt_1'] = key_encrypt1
                            context['key_encrypt_2'] = key_encrypt2
                            context['key_encrypt_3'] = key_encrypt3
                            context['ctr_encrypt'] = ctr_encrypt
                            context['encrypted_ctr']=True
                            count_falla=0
                    except:
                        pass
                
                #decrypt in CTR MODE
                if 'Decrypt_CTR' in request.POST:
                    try:
                        try:
                            key_decrypt_1 = request.POST.get("key_decrypt_1")
                            key_decrypt_2 = request.POST.get("key_decrypt_2")
                            key_decrypt_3 = request.POST.get("key_decrypt_3")
                            ctr_decrypt = request.POST.get("ctr_decrypt")

                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt_1 = key_decrypt_1.upper()
                            key_decrypt_2 = key_decrypt_2.upper()
                            key_decrypt_3 = key_decrypt_3.upper()
                            ctr_decrypt = ctr_decrypt.upper()
                            decode = decode_tdes_image_ctr(key_decrypt_1, key_decrypt_2, key_decrypt_3, ctr_decrypt, 'static/images/clean.png')
                        except:
                            decode=-1
                        if decode == -1:
                            context['mistake_decrypt_ctr']=True
                        else:
                            context['key_decrypt_1']=key_decrypt_1
                            context['key_decrypt_2']=key_decrypt_2
                            context['key_decrypt_3']=key_decrypt_3
                            context['ctr_decrypt']=ctr_decrypt
                            context['decrypted_ctr']=True
                    except:
                        pass
        
        ##AES CYPHER
        elif name == "AES":
            view = "aes.html"
            if request.method == "POST":
                #encrypt in ECB MODE
                if 'Encrypt_ECB' in request.POST:
                    key_encrypt_hex = request.POST.get("key_encrypt")

                    url = request.POST.get("url")
                    try:
                        key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                        encode = encode_aes_image_ecb(key_encrypt, url)
                        if encode == -1:
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt_hex = randomkeyhexa32()
                                key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                                context['failed_encrypt_ecb']=True
                                context['key_encrypt'] = key_encrypt_hex
                                encode = encode_aes_image_ecb(key_encrypt, url)
                                context['encrypted_ecb']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_ecb']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt'] = key_encrypt_hex
                            context['encrypted_ecb']=True
                            count_falla=0
                    except:
                        pass
                    
                #decrypt in ECB MODE
                if 'Decrypt_ECB' in request.POST:
                    try:
                        try:
                            key_decrypt_hex = request.POST.get("key_decrypt")
                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt = codecs.decode(key_decrypt_hex, 'hex_codec')
                            decode = decode_aes_image_ecb(key_decrypt, 'static/images/clean.png')
                        except:
                            decode= -1
                        if decode == -1:
                            context['mistake_decrypt_ecb']=True
                        else:
                            context['key_decrypt']=key_decrypt_hex
                            context['decrypted_ecb']=True
                    except:
                        pass
                
                #encrypt in CBC MODE
                if 'Encrypt_CBC' in request.POST:
                    key_encrypt_hex = request.POST.get("key_encrypt")
                    iv_encrypt_hex = request.POST.get("iv_encrypt")

                    url = request.POST.get("url")
                    try:
                        key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                        if iv_encrypt_hex != "":
                            iv_encrypt = codecs.decode(iv_encrypt_hex, 'hex_codec')
                        else:
                            iv_encrypt = None
                        iv_encrypt = encode_aes_image_cbc(key_encrypt, url, iv_encrypt)
                        if iv_encrypt == -1:
                            context['mistake_encrypt_cbc']=True
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt_hex = randomkeyhexa32()
                                key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                                iv_encrypt = None
                                iv_encrypt = encode_aes_image_cbc(key_encrypt, url, iv_encrypt)
                                context['failed_encrypt_cbc']=True
                                context['iv_encrypt'] = iv_encrypt.upper()
                                context['key_encrypt'] = key_encrypt_hex
                                context['encrypted_cbc']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_cbc']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt'] = key_encrypt_hex
                            context['iv_encrypt'] = iv_encrypt.upper()
                            context['encrypted_cbc']=True
                            count_falla=0
                    except:
                        pass
              
                #decrypt in CBC MODE
                if 'Decrypt_CBC' in request.POST:
                    try:
                        try:
                            key_decrypt_hex = request.POST.get("key_decrypt")
                            iv_decrypt_hex = request.POST.get("iv_decrypt")

                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt = codecs.decode(key_decrypt_hex, 'hex_codec')
                            iv_decrypt = codecs.decode(iv_decrypt_hex, 'hex_codec')
                            decode = decode_aes_image_cbc(key_decrypt, 'static/images/clean.png', iv_decrypt)
                        except:
                            decode= -1
                        if decode == -1:
                            context['mistake_decrypt_cbc']=True
                        else:
                            context['key_decrypt']=key_decrypt_hex
                            context['iv_decrypt']=iv_decrypt_hex
                            context['decrypted_cbc']=True
                    except:
                        pass
                
                #encrypt in OFB MODE
                if 'Encrypt_OFB' in request.POST:
                    key_encrypt_hex = request.POST.get("key_encrypt")
                    iv_encrypt_hex = request.POST.get("iv_encrypt")

                    url = request.POST.get("url")
                    try:
                        key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                        if iv_encrypt_hex != "":
                            iv_encrypt = codecs.decode(iv_encrypt_hex, 'hex_codec')
                        else:
                            iv_encrypt = None
                        iv_encrypt = encode_aes_image_ofb(key_encrypt, url, iv_encrypt)
                        if iv_encrypt == -1:
                            context['mistake_encrypt_ofb']=True
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt_hex = randomkeyhexa32()
                                key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                                iv_encrypt = None
                                iv_encrypt = encode_aes_image_ofb(key_encrypt, url, iv_encrypt)
                                context['failed_encrypt_ofb']=True
                                context['iv_encrypt'] = iv_encrypt.upper()
                                context['key_encrypt'] = key_encrypt_hex
                                context['encrypted_ofb']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_ofb']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt'] = key_encrypt_hex
                            context['iv_encrypt'] = iv_encrypt.upper()
                            context['encrypted_ofb']=True
                            count_falla=0
                    except:
                        pass
    
                #decrypt in OFB MODE
                if 'Decrypt_OFB' in request.POST:
                    try:
                        try:
                            key_decrypt_hex = request.POST.get("key_decrypt")
                            iv_decrypt_hex = request.POST.get("iv_decrypt")

                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt = codecs.decode(key_decrypt_hex, 'hex_codec')
                            iv_decrypt = codecs.decode(iv_decrypt_hex, 'hex_codec')
                            decode = decode_aes_image_ofb(key_decrypt, 'static/images/clean.png', iv_decrypt)
                        except:
                            decode= -1
                        if decode == -1:
                            context['mistake_decrypt_ofb']=True
                        else:
                            context['key_decrypt']=key_decrypt_hex
                            context['iv_decrypt']=iv_decrypt_hex
                            context['decrypted_ofb']=True
                    except:
                        pass
                
                #encrypt in CFB MODE
                if 'Encrypt_CFB' in request.POST:
                    key_encrypt_hex = request.POST.get("key_encrypt")
                    iv_encrypt_hex = request.POST.get("iv_encrypt")

                    url = request.POST.get("url")
                    try:
                        key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                        if iv_encrypt_hex != "":
                            iv_encrypt = codecs.decode(iv_encrypt_hex, 'hex_codec')
                        else:
                            iv_encrypt = None
                        iv_encrypt = encode_aes_image_cfb(key_encrypt, url, iv_encrypt)
                        if iv_encrypt == -1:
                            context['mistake_encrypt_cfb']=True
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt_hex = randomkeyhexa32()
                                key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                                iv_encrypt = None
                                iv_encrypt = encode_aes_image_cfb(key_encrypt, url, iv_encrypt)
                                context['failed_encrypt_cfb']=True
                                context['iv_encrypt'] = iv_encrypt.upper()
                                context['key_encrypt'] = key_encrypt_hex
                                context['encrypted_cfb']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_cfb']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt'] = key_encrypt_hex
                            context['iv_encrypt'] = iv_encrypt.upper()
                            context['encrypted_cfb']=True
                            count_falla=0
                    except:
                        pass

                
                #decrypt in CFB MODE
                if 'Decrypt_CFB' in request.POST:
                    try:
                        try:
                            key_decrypt_hex = request.POST.get("key_decrypt")
                            iv_decrypt_hex = request.POST.get("iv_decrypt")

                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt = codecs.decode(key_decrypt_hex, 'hex_codec')
                            iv_decrypt = codecs.decode(iv_decrypt_hex, 'hex_codec')
                            decode = decode_aes_image_cfb(key_decrypt, 'static/images/clean.png', iv_decrypt)
                        except:
                            decode= -1
                        if decode == -1:
                            context['mistake_decrypt_cfb']=True
                        else:
                            context['key_decrypt']=key_decrypt_hex
                            context['iv_decrypt']=iv_decrypt_hex
                            context['decrypted_cfb']=True
                    except:
                        pass
                
                #encrypt in CTR MODE
                if 'Encrypt_CTR' in request.POST:
                    key_encrypt_hex = request.POST.get("key_encrypt")
                    nonce_encrypt_hex = request.POST.get("nonce_encrypt")

                    url = request.POST.get("url")
                    try:
                        key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                        if nonce_encrypt_hex != "":
                            nonce_encrypt = codecs.decode(nonce_encrypt_hex, 'hex_codec')
                        else:
                            nonce_encrypt = None
                        nonce_encrypt = encode_aes_image_ctr(key_encrypt, url, nonce_encrypt)
                        if nonce_encrypt == -1:
                            context['mistake_encrypt_ctr']=True
                            count_falla=count_falla+1
                            if count_falla>=3:
                                key_encrypt_hex = randomkeyhexa32()
                                key_encrypt = codecs.decode(key_encrypt_hex, 'hex_codec')
                                nonce_encrypt = None
                                nonce_encrypt = encode_aes_image_ctr(key_encrypt, url, nonce_encrypt)
                                context['failed_encrypt_ctr']=True
                                context['nonce_encrypt'] = nonce_encrypt.upper()
                                context['key_encrypt'] = key_encrypt_hex
                                context['encrypted_ctr']=True
                                count_falla=0 
                            else:
                                context['mistake_encrypt_ctr']=True
                                context['countfail']=count_falla
                        else:
                            context['key_encrypt'] = key_encrypt_hex
                            context['nonce_encrypt'] = nonce_encrypt.upper()
                            context['encrypted_ctr']=True
                            count_falla=0
                    except:
                        pass

                #decrypt in CTR MODE
                if 'Decrypt_CTR' in request.POST:
                    try:
                        try:
                            key_decrypt_hex = request.POST.get("key_decrypt")
                            nonce_decrypt_hex = request.POST.get("nonce_decrypt")

                            if os.path.exists("static/images/clean.png"):
                                os.remove("static/images/clean.png")
                            upload = request.FILES.get("im1")
                            fss = FileSystemStorage()
                            fss.save('static/images/clean.png', upload)
                            key_decrypt = codecs.decode(key_decrypt_hex, 'hex_codec')
                            nonce_decrypt = codecs.decode(nonce_decrypt_hex, 'hex_codec')
                            decode = decode_aes_image_ctr(key_decrypt, 'static/images/clean.png', nonce_decrypt)
                        except:
                            decode= -1
                        if decode == -1:
                            context['mistake_decrypt_ctr']=True
                        else:
                            context['key_decrypt']=key_decrypt_hex
                            context['nonce_decrypt']=nonce_decrypt_hex
                            context['decrypted_ctr']=True
                    except:
                        pass

        ##GAMMA PENTAGONAL
        elif name == "Gamma pentagonal":
            view = "gammapentagonal.html"
            if request.method == "POST":
                
                #editar grafo
                actualizar = request.POST.get("actualizar")
                try:
                    if actualizar == "Actualizar":
                        x = request.POST.get("x")
                        y = request.POST.get("y")
                        permutacion = request.POST.get("permutacion")
                        aleatoria = request.POST.get("aleatoria")
                        if aleatoria == "on":
                            grafo, permutacion= nuevoGrafoAlt(x, y)
                        else:
                            permutacion=convertirPermutacion(permutacion)
                            grafo = nuevoGrafo(x, y, permutacion)
                        if grafo == -1:
                                count_falla=count_falla+1
                                if count_falla>=3:
                                    context['failed_graph']=True
                                    count_falla=0
                                    x, y = generarPunto()
                                    grafo, permutacion= nuevoGrafoAlt(x, y)
                                else:
                                    context['mistake_graph']=True
                                    context['countfail']=count_falla
                        else:
                            count_falla=0
                            vectores = grafo
                except:
                    pass
                
                
                #encrypt
                encrypt = request.POST.get("encrypt")
                try:
                    if encrypt == "Encrypt":
                        cleartext = request.POST.get("cleartext")
                        encode = gammaencript(cleartext, permutacion, vectores)
                        if encode == -1:
                                count_falla=count_falla+1
                                if count_falla>=3:
                                    context['failed_encrypt']=True
                                    count_falla=0
                                else:
                                    context['mistake_encrypt']=True
                                    context['countfail']=count_falla
                        else:
                            count_falla=0
                            context['encrypted']=True
                            context['cleartext']=cleartext
                            context['encodedtext']=encode
                except:
                    pass
                    
                    
                #decrypt
                decrypt = request.POST.get("decrypt")
                try:
                    if decrypt == "Decrypt":
                        codedtext = request.POST.get("codedtext")
                        decode = gammadecript(codedtext, permutacion, vectores)
                        if decode == -1:
                                count_falla=count_falla+1
                                if count_falla>=3:
                                    context['failed_decrypt']=True
                                    count_falla=0
                                else:
                                    context['mistake_decrypt']=True
                                    context['countfail']=count_falla
                        else:
                            count_falla=0
                            context['decrypted']=True
                            context['cleartext']=decode
                            context['encodedtext']=codedtext
                except:
                    pass
                

                
    return render(request, view, context=context)

