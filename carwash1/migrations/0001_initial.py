# Generated by Django 4.2.3 on 2024-08-12 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('imagen', models.ImageField(null=True, upload_to='CERTIFICADOS')),
            ],
        ),
        migrations.CreateModel(
            name='Ingreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patente', models.CharField(max_length=8)),
                ('vehiculo', models.CharField(choices=[('CITYCAR', 'City Car'), ('SEDAN', 'Sedán'), ('HATCHBACK', 'Hatchback'), ('SUV', 'SUV'), ('CAMIONETA', 'Camioneta'), ('XL', 'XL')], max_length=20)),
                ('lavado', models.CharField(choices=[('EXPRESS', 'Express'), ('FULL', 'Full')], max_length=10)),
                ('tipo_de_pago', models.CharField(choices=[('CREDITO', 'Crédito'), ('DEBITO', 'Débito'), ('EFECTIVO', 'Efectivo'), ('TRANSFERENCIA', 'Transferencia')], max_length=20)),
                ('valor', models.IntegerField()),
                ('propina', models.DecimalField(decimal_places=0, max_digits=10)),
                ('contacto', models.CharField(max_length=50)),
                ('correo', models.EmailField(blank=True, max_length=254, null=True)),
                ('estado_vehiculo', models.CharField(choices=[('POR REALIZAR', 'Por Realizar'), ('TERMINADO', 'Terminado')], default='POR REALIZAR', max_length=15)),
                ('tipo_doc', models.CharField(choices=[('BOLETA', 'Boleta'), ('FACTURA', 'Factura')], max_length=10)),
                ('estado_factura', models.CharField(choices=[('SIN FACTURA', 'Sin Factura'), ('POR EMITIR', 'Por Emitir'), ('EMITIDA', 'Emitida')], default='SIN FACTURA', max_length=15)),
                ('Rut', models.CharField(blank=True, max_length=15, null=True)),
                ('fecha_ingreso', models.DateTimeField(auto_now_add=True)),
                ('cliente_acepta', models.BooleanField(default=False)),
                ('firma_electronica', models.CharField(blank=True, max_length=1000000, null=True)),
                ('comentario', models.CharField(blank=True, default='Sin Comentario', max_length=1000000, null=True)),
            ],
            options={
                'ordering': ['-fecha_ingreso'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nombre', models.CharField(default='', max_length=256)),
                ('Correo_Electronico', models.EmailField(default='', max_length=254, unique=True)),
                ('fecha', models.DateTimeField()),
                ('vehiculo', models.CharField(choices=[('City Car', 'Citycar'), ('Sedan', 'Sedan'), ('Suv', 'Suv'), ('Camioneta', 'Camioneta'), ('XL', 'Xl'), ('Recargo', 'Recargo')], default='City Car', max_length=15)),
                ('lavado', models.CharField(choices=[('Express', 'Express'), ('Full', 'Full')], default='Express', max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
