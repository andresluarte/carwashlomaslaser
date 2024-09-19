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
        required=True  # Puede ser True o False
    )

    class Meta:
        model = Ingreso
        fields = ['patente', 'vehiculo', 'lavado', 'tipo_de_pago', 'valor', 'propina', 'contacto', 'correo', 'tipo_doc', 'Rut', 'firma_electronica', 'cliente_acepta']

    def clean_patente(self):
        patente = self.cleaned_data.get('patente')
        if patente:
            patente = patente.upper().replace(' ', '')
            if len(patente) != 8:
                raise forms.ValidationError("La patente debe tener exactamente 8 caracteres, incluyendo guiones.")
            if patente[2] != '-' or patente[5] != '-':
                raise forms.ValidationError("El formato de la patente debe ser XX-XX-XX.")
            return patente
        else:
            raise forms.ValidationError("La patente no puede estar vacía.")


    def clean(self):
        cleaned_data = super().clean()
        tipo_doc = cleaned_data.get('tipo_doc')
        rut = cleaned_data.get('Rut')

        if tipo_doc == 'FACTURA' and not rut:
            self.add_error('Rut', 'El RUT es obligatorio si se selecciona "Factura".')
        elif rut and tipo_doc != 'FACTURA':
            self.add_error('Rut', 'El RUT no debe ser ingresado si no es "Factura".')

        return cleaned_data

    def clean_cliente_acepta(self):
        cliente_acepta = self.cleaned_data.get('cliente_acepta')
        if cliente_acepta is None:
            raise forms.ValidationError("Debe aceptar la declaración del cliente.")
        return cliente_acepta

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
        choices=[('SIN FACTURA', 'Sin Factura'), ('POR EMITIR', 'Por Emitir'), ('EMITIDA', 'Emitida')],
        required=False
    )
    estado_vehiculo = forms.ChoiceField(
        label='Estado Vehículo', 
        choices=[('POR REALIZAR', 'Por Realizar'), ('TERMINADO', 'Terminado')],
        required=False
    )
    Rut = forms.CharField(
        label='RUT', 
        max_length=15, 
        required=False
    )
    contacto = forms.CharField(
        label='Contacto Telefónico', 
        max_length=50, 
        required=False
    )
    comentario = forms.CharField(
        label='Comentario', 
        required=False
    )

    class Meta:
        model = Ingreso
        fields = ['estado_factura', 'estado_vehiculo', 'tipo_de_pago', 'tipo_doc', 'Rut', 'contacto', 'comentario']

    def clean(self):
        cleaned_data = super().clean()
        tipo_doc = self.cleaned_data.get('tipo_doc')  # Obtener el tipo de documento actual del ingreso
        rut = cleaned_data.get('Rut')
        estado_factura = cleaned_data.get('estado_factura')

        # Validación según el tipo de documento
        if tipo_doc == 'FACTURA':
            if not rut:
                self.add_error('Rut', 'El RUT es obligatorio si se selecciona "Factura".')
        else:
            if rut:
                self.add_error('Rut', 'El RUT no debe ser ingresado si no es "Factura".')
            if estado_factura and estado_factura != 'SIN FACTURA':
                self.add_error('estado_factura', 'El estado de la factura no debe ser modificado si no es "Factura".')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tipo_doc = self.instance.tipo_doc  # Obtener el tipo de documento actual del ingreso
        tipo_de_pago = self.instance.tipo_de_pago  # Obtener el tipo de pago actual del ingreso

        # Lógica para habilitar/deshabilitar campos basado en 'tipo_doc' y 'tipo_de_pago'
        if tipo_doc != 'FACTURA':
            self.fields['estado_factura'].widget.attrs['disabled'] = 'disabled'
            self.fields['Rut'].widget.attrs['disabled'] = 'disabled'
        else:
            self.fields['estado_factura'].widget.attrs.pop('disabled', None)  # Elimina 'disabled'
            self.fields['Rut'].widget.attrs.pop('disabled', None)  # Elimina 'disabled'

