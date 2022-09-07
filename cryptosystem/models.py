from django.db import models

# Create your models here.
class Cryptosystem(models.Model):
    name = models.TextField()
    description = models.TextField()