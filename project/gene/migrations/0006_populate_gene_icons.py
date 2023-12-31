# Generated by Django 4.2.3 on 2023-07-25 23:15

from django.db import migrations
from gene.utils import generate_icon_path

def set_icons(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Gene = apps.get_model("gene", "Gene")
    db_alias = schema_editor.connection.alias
    object_list = []
    for gene in Gene.objects.using(db_alias).all():
        gene.icon = generate_icon_path(gene)
        object_list.append(gene)
    Gene.objects.using(db_alias).bulk_update(object_list, ['icon'])


def unset_icons(apps, schema_editor):
    pass  # no need

class Migration(migrations.Migration):

    dependencies = [
        ('gene', '0005_gene_icon'),
    ]

    operations = [
        migrations.RunPython(set_icons, unset_icons)
    ]
