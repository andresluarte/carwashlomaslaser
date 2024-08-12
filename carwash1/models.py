import imp
from pydoc import render_doc
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.utils.timezone import datetime
from django.core.exceptions import ValidationError


# Create your models here.
from django.db import models

from django.db import models

#formato rut chileno 
import re
from django.core.exceptions import ValidationError


import re
from django.core.exceptions import ValidationError


class Ingreso(models.Model):
    VEHICULO_CHOICES = [
        ('CITYCAR', 'City Car'),
        ('SEDAN', 'Sedán'),
        ('HATCHBACK', 'Hatchback'),
        ('SUV', 'SUV'),
        ('CAMIONETA', 'Camioneta'),
        ('XL', 'XL')
    ]

    LAVADO_CHOICES = [
        ('EXPRESS', 'Express'),
        ('FULL', 'Full')
    ]

    TIPO_PAGO_CHOICES = [
        ('CREDITO', 'Crédito'),
        ('DEBITO', 'Débito'),
        ('EFECTIVO', 'Efectivo'),
        ('TRANSFERENCIA', 'Transferencia')
    ]

    TIPO_DOC_CHOICES = [
        ('BOLETA', 'Boleta'),
        ('FACTURA', 'Factura')
    ]

    ESTADO_VEHICULO_CHOICES = [
        ('POR REALIZAR', 'Por Realizar'),
        ('TERMINADO', 'Terminado')
    ]

    ESTADO_FACTURA_CHOICES = [
        ('SIN FACTURA', 'Sin Factura'),
        ('POR EMITIR', 'Por Emitir'),
        ('EMITIDA', 'Emitida')
    ]

    patente = models.CharField(max_length=8)
    vehiculo = models.CharField(max_length=20, choices=VEHICULO_CHOICES)
    lavado = models.CharField(max_length=10, choices=LAVADO_CHOICES)
    tipo_de_pago = models.CharField(max_length=20, choices=TIPO_PAGO_CHOICES)
    valor = models.IntegerField()
    propina = models.DecimalField(max_digits=10, decimal_places=0)
    contacto = models.CharField(max_length=15)
    correo = models.EmailField(blank=True, null=True)
    estado_vehiculo = models.CharField(max_length=15, choices=ESTADO_VEHICULO_CHOICES, default='POR REALIZAR')
    tipo_doc = models.CharField(max_length=10, choices=TIPO_DOC_CHOICES)
    estado_factura = models.CharField(max_length=15, choices=ESTADO_FACTURA_CHOICES, default='SIN FACTURA')
    Rut = models.CharField(max_length=15, blank=True, null=True)
    fecha_ingreso = models.DateTimeField(auto_now_add=True)
    cliente_acepta = models.BooleanField(default=False)
    firma_electronica = models.CharField(max_length=1000000, blank=True, null=True)
    comentario = models.CharField(max_length=1000000, blank=True, null=True,default="Sin Comentario")
    class Meta:
        ordering = ['-fecha_ingreso']

    def clean(self):
        if len(self.patente) != 8:
            raise ValidationError("La patente debe tener exactamente 8 caracteres, incluyendo guiones.")
        # Verificar el formato XX-XX-XX
        if self.patente[2] != '-' or self.patente[5] != '-':
            raise ValidationError("El formato de la patente debe ser XX-XX-XX.")
        if self.tipo_doc == 'FACTURA' and not self.Rut:
            raise ValidationError("El RUT es obligatorio si se selecciona 'Factura'.")
        if self.tipo_doc != 'FACTURA' and self.Rut:
            raise ValidationError("El RUT no debe ser ingresado si no es 'Factura'.")

    def __str__(self):
        return f"{self.patente} - {self.vehiculo} - {self.lavado}"



class Certificado(models.Model):
    nombre = models.CharField(max_length=20)
    imagen  = models.ImageField(upload_to="CERTIFICADOS",null=True)

    def __str__(self) :
        return self.Nombre
    

class Reserva(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    Nombre = models.CharField(max_length=256, default='', blank=False)
    Correo_Electronico = models.EmailField(unique=True, blank=False,default='')
    fecha = models.DateTimeField()


    class Vehiculo(models.TextChoices):
        CityCar =  "City Car"
        Sedan = "Sedan"
        Suv =  "Suv"
        Camioneta = "Camioneta"
        XL ="XL"
        Recargo = "Recargo"

        # (...)

    vehiculo = models.CharField(
        max_length=15,
        choices=Vehiculo.choices,
        default=Vehiculo.CityCar
    )
    
    class Lavado(models.TextChoices):
        Express =  "Express"
        Full =  "Full"
        

        # (...)

    lavado = models.CharField(
        max_length=15,
        choices=Lavado.choices,
        default=Lavado.Express
    )



   
    


