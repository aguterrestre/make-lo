# Generated manually to load initial data

from django.db import migrations


def load_initial_data(apps, schema_editor):
    """
    Función para cargar datos iniciales básicos necesarios para el funcionamiento
    del sistema. Crea registros con IDs específicos que son referenciados por
    los modelos con default=1.
    """
    Sale_Condition = apps.get_model('sale', 'Sale_Condition')
    Client_Status = apps.get_model('sale', 'Client_Status')
    Client = apps.get_model('sale', 'Client')
    City = apps.get_model('sale', 'City')
    
    # Crear condiciones de venta básicas
    Sale_Condition.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Contado',
            'internal_code': 'CONT',
            'description': 'Pago al contado'
        }
    )
    Sale_Condition.objects.get_or_create(
        id=2,
        defaults={
            'name': 'Cuenta Corriente',
            'internal_code': 'CC',
            'description': 'Cuenta corriente'
        }
    )
    Sale_Condition.objects.get_or_create(
        id=3,
        defaults={
            'name': 'A 30 días',
            'internal_code': '30D',
            'description': 'Pago a 30 días'
        }
    )
    
    # Crear estados de cliente básicos
    Client_Status.objects.get_or_create(
        id=1,
        defaults={
            'name': 'Activo',
            'description': 'Cliente activo'
        }
    )
    Client_Status.objects.get_or_create(
        id=2,
        defaults={
            'name': 'Inactivo',
            'description': 'Cliente inactivo'
        }
    )
    
    # Crear cliente "Consumidor Final"
    # Verificar que la ciudad con id=1 existe (debe estar cargada desde fixtures)
    city = City.objects.filter(id=1).first()
    if city:
        # Obtener DocumentType con id=96 (django_afip.DocumentType)
        DocumentType = apps.get_model('afip', 'DocumentType')
        document_type = DocumentType.objects.filter(id=96).first()
        
        Client.objects.get_or_create(
            id=1,
            defaults={
                'name': 'Consumidor',
                'surname': 'Final',
                'business_name': 'Consumidor Final',
                'trade_name': 'Consumidor Final',
                'document': '0',
                'document_type': document_type,  # DocumentType id=96
                'fiscal_condition': 'Consumidor Final',
                'residence_city': city,
                'sale_condition_id': 1,  # Contado
                'status_id': 1,  # Activo
                'gender': 'male',
                'address': '',
                'comercial_address': '',
            }
        )


def reverse_load_initial_data(apps, schema_editor):
    """
    Función para revertir la carga de datos. Elimina los registros creados.
    """
    Sale_Condition = apps.get_model('sale', 'Sale_Condition')
    Client_Status = apps.get_model('sale', 'Client_Status')
    Client = apps.get_model('sale', 'Client')
    
    # Eliminar cliente "Consumidor Final"
    Client.objects.filter(id=1).delete()
    
    # Eliminar condiciones de venta
    Sale_Condition.objects.filter(id__in=[1, 2, 3]).delete()
    
    # Eliminar estados de cliente
    Client_Status.objects.filter(id__in=[1, 2]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0005_auto_20210223_0856'),
    ]

    operations = [
        migrations.RunPython(load_initial_data, reverse_load_initial_data),
    ]

