from django.db import migrations


def create_departments(apps, schema_editor):
    # On récupère le modèle via 'apps' pour être sûr d'utiliser la bonne version
    Department = apps.get_model('ticket', 'Department')

    departments = [
        {'name': 'Technique', 'description': 'Problèmes matériels et logiciels'},
        {'name': 'Facturation', 'description': 'Paiements, factures et abonnements'},
        {'name': 'Commercial', 'description': 'Demandes d\'achat et devis'},
        {'name': 'SAV', 'description': 'Service après-vente et retours'},
    ]

    for dep in departments:
        Department.objects.get_or_create(name=dep['name'], defaults={'description': dep['description']})


class Migration(migrations.Migration):
    dependencies = [
        ('ticket', '0001_initial'),  # Doit correspondre au nom de ta première migration
    ]

    operations = [
        migrations.RunPython(create_departments),
    ]