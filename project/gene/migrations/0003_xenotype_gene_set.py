# Generated by Django 4.2.3 on 2023-07-25 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gene', '0002_build_defaults'),
    ]

    operations = [
        migrations.AddField(
            model_name='xenotype',
            name='gene_set',
            field=models.ManyToManyField(related_name='xenotype_set', to='gene.gene'),
        ),
    ]
