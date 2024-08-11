from django.contrib import admin

# Register your models here.
from .models import Ingreso,Certificado,Reserva


admin.site.register(Ingreso)

admin.site.register(Certificado)
admin.site.register(Reserva)