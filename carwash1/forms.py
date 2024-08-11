from ast import arg
from audioop import add
from dataclasses import fields
from pyexpat import model
from django import forms 
from .models import Ingreso,Reserva
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.utils.timezone import datetime
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
import base64


class IngresoForm(forms.ModelForm):
    valor = forms.IntegerField(
        label='Valor', 
        min_value=1000, 
        max_value=50000, 
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )
    propina = forms.DecimalField(
        label='Propina', 
        max_digits=10, 
        decimal_places=0, 
        
    )
    contacto = forms.CharField(
        label='Contacto Telefónico', 
        required=False
    )
    correo = forms.EmailField(
        label='Correo Electrónico', 
        required=False
    )
    tipo_doc = forms.ChoiceField(
        label='Tipo Documento', 
        choices=[('BOLETA', 'Boleta'), ('FACTURA', 'Factura')]
    )
    Rut = forms.CharField(
        label='RUT', 
        max_length=15, 
        required=False
    )
    firma_electronica = forms.CharField(
        label='Firma Electrónica', 
        widget=forms.HiddenInput(),  # Placeholder para la firma electrónica en formato base64
        required=False
    )
    cliente_acepta = forms.BooleanField(
        label='Cliente Acepta', 
        required=False
    )

    class Meta:
        model = Ingreso
        fields = ['patente', 'vehiculo', 'lavado', 'tipo_de_pago', 'valor', 'propina', 'contacto', 'correo', 'tipo_doc', 'Rut', 'firma_electronica', 'cliente_acepta']

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')
        if patente:
            patente = patente.upper().replace(' ', '')
            # Verificar que la patente tenga exactamente 8 caracteres incluyendo guiones
            if len(patente) != 8:
                raise forms.ValidationError("La patente debe tener exactamente 8 caracteres, incluyendo guiones.")
            # Asegurarse de que el formato sea XX-XX-XX
            if patente[2] != '-' or patente[5] != '-':
                raise forms.ValidationError("El formato de la patente debe ser XX-XX-XX.")
            return patente
        return patente

    def clean(self):
        cleaned_data = super().clean()
        tipo_doc = cleaned_data.get('tipo_doc')
        rut = cleaned_data.get('Rut')

        if tipo_doc == 'FACTURA' and not rut:
            self.add_error('Rut', 'El RUT es obligatorio si se selecciona "Factura".')
        elif rut and tipo_doc != 'FACTURA':
            self.add_error('Rut', 'El RUT no debe ser ingresado si no es "Factura".')

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        tipo_doc = self.cleaned_data.get('tipo_doc')

        if tipo_doc == 'FACTURA':
            instance.estado_factura = 'POR EMITIR'
        else:
            instance.estado_factura = 'SIN FACTURA'

        instance.estado_vehiculo = 'POR REALIZAR'
        instance.firma_electronica = self.cleaned_data.get('firma_electronica', '')

        if commit:
            instance.save()
        return instance
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields=["username","first_name","last_name","email","password1","password2"]
            

    
    pass


class ReservaForm(forms.ModelForm):
    
    

   

    #patente = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
   
    
   


    class Meta:
        model = Reserva
        fields = '__all__'

class IngresoUpdateForm(forms.ModelForm):
    estado_factura = forms.ChoiceField(
        label='Estado Factura', 
        choices=[('SIN FACTURA', 'Sin Factura'), ('POR EMITIR', 'Por Emitir'), ('EMITIIDA', 'Emitida')]
        
    )
    estado_vehiculo = forms.ChoiceField(
        label='Estado Vehículo', 
        choices=[('POR REALIZAR', 'Por Realizar'), ('TERMINADO', 'Terminado')]
    )
    Rut = forms.CharField(
        label='RUT', 
        max_length=15, 
        required=False
    )
    contacto = forms.CharField(
        label='Contacto Telefónico', 
        max_length=15, 
        required=False
    )
    comentario = forms.CharField(
        label='Comentario', 
        required=False
    )

    class Meta:
        model = Ingreso
        fields = ['estado_factura', 'estado_vehiculo', 'Rut', 'contacto','comentario']

    def clean(self):
        cleaned_data = super().clean()
        tipo_doc = self.instance.tipo_doc  # Obtener el tipo de documento actual del ingreso

        rut = cleaned_data.get('Rut')
        if tipo_doc == 'FACTURA' and not rut:
            self.add_error('Rut', 'El RUT es obligatorio si se selecciona "Factura".')
        elif rut and tipo_doc != 'FACTURA':
            self.add_error('Rut', 'El RUT no debe ser ingresado si no es "Factura".')

        return cleaned_data