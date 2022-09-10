from django.contrib import admin

# Register your models here.
from .models import Cryptosystem

class CryptosystemAdmin(admin.ModelAdmin):
    list_display=['id', 'name']

admin.site.register(Cryptosystem, CryptosystemAdmin)