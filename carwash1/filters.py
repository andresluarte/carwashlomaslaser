
import django_filters
from .models import Ingreso
import django_filters
from django import forms
class FilterIngreso(django_filters.FilterSet):
    estado_vehiculo = django_filters.ChoiceFilter(label='Estado Vehiculo', choices=Ingreso.ESTADO_VEHICULO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    patente = django_filters.CharFilter(label='Patente', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo_de_pago = django_filters.ChoiceFilter(label='Tipo de Pago', choices=Ingreso.TIPO_PAGO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_doc = django_filters.ChoiceFilter(label='Tipo Documento', choices=Ingreso.TIPO_DOC_CHOICES, widget=forms.Select(attrs={'class': 'form-control'})) 
    lavado = django_filters.ChoiceFilter(label='Lavado', choices=Ingreso.LAVADO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    vehiculo = django_filters.ChoiceFilter(label='Vehículo', choices=Ingreso.VEHICULO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    estado_vehiculo = django_filters.ChoiceFilter(label='Estado Vehiculo', choices=Ingreso.ESTADO_VEHICULO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    fecha_ingreso = django_filters.DateFromToRangeFilter(
        label='Fecha de Ingreso',
        widget=django_filters.widgets.RangeWidget(attrs={'class': 'form-control', 'type': 'date'})
    )
    class Meta:
        model = Ingreso
        fields = ['patente', 'tipo_de_pago', 'tipo_doc', 'lavado', 'vehiculo','estado_vehiculo','fecha_ingreso']