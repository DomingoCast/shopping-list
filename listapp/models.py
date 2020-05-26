from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null = True, on_delete=models.CASCADE)
    name = models.CharField( max_length=200, null = True)
    email = models.CharField( max_length=200, null = True)
    phone = models.CharField( max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if not self.name:
            return 'none'
        return self.name

class Item(models.Model):
    STATUS = (
        ('Por comprar', 'Por comprar'),
        ('Comprando', 'Comprando'),
        ('Comprado', 'Comprado'),
        )
    status = models.CharField(max_length=200, null = True, choices = STATUS)
    name = models.CharField( max_length=200, null = True)
    store = models.CharField( max_length=200, null = True)
    quantity = models.PositiveIntegerField( null = True)
    aditional_info = models.CharField( max_length=200, null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add=True, null = True)
    def __str__(self):
        return self.name
        
class Lista(models.Model):
    STATUS = (
        ('Por comprar', 'Por comprar'),
        ('Comprando', 'Comprando'),
        ('Comprado', 'Comprado'),
        )
    item = models.ManyToManyField(Item)#, null = True, on_delete = models.SET_NULL)

    status = models.CharField(max_length=200, null = True, choices = STATUS)
    name = models.CharField( max_length=200, null = True)
    def __str__(self):
        return self.name
    


class Familia(models.Model):
    lista =models.ManyToManyField(Lista)
    name = models.CharField( max_length=200, null = True)
    miembro = models.ManyToManyField(Customer)#, null = True, on_delete = models.SET_NULL)
    def __str__(self):
        return self.name

