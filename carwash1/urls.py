import imp
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import inicio,ingreso,contacto,tabla_ingresos,modificar_ingreso,eliminar_ingreso,registro,reserva,export_ingresos_to_excel

urlpatterns = [
    path('inicio', inicio , name = "home"),
    path('ingreso/', ingreso , name = "ingreso"),
    path('contacto/', contacto , name = "contacto"),
    path('tabla_ingresos/', tabla_ingresos , name = "tabla_ingresos"),
    path('modificar_ingreso/<id>/', modificar_ingreso , name = "modificar_ingreso"),
    path('eliminar_ingreso/<id>/', eliminar_ingreso , name = "eliminar_ingreso"),
    path('registro', registro, name="registro"),
    path('reserva', reserva, name="reserva"),
    path('exportar_ingresos/', export_ingresos_to_excel, name='export_ingresos_to_excel'),




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
