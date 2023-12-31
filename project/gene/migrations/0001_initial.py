# Generated by Django 4.1.6 on 2023-07-25 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Colony',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('def_name', models.CharField(max_length=50)),
                ('vanilla', models.BooleanField(default=False)),
                ('category', models.CharField(
                    choices=[('ARCHITE', 'Archite'), ('SPECIAL_ABILITIES', 'Special abilities'), ('HEMOGEN', 'Hemogen'),
                             ('HEALTH', 'Health'), ('PSYCHIC', 'Psychic'), ('MOVEMENT', 'Movement'), ('MOOD', 'Mood'),
                             ('TEMPERATURE', 'Temperature'),
                             ('RESISTANCE_AND_SENSITIVITY', 'Resistance and sensitivity'), ('VIOLENCE', 'Violence'),
                             ('SLEEP', 'Sleep'), ('PAIN', 'Pain'), ('REPRODUCTION', 'Reproduction'),
                             ('BEAUTY', 'Beauty'), ('COSMETIC', 'Cosmetic'), ('APTITUDES', 'Aptitudes'),
                             ('DRUGS', 'Drugs'), ('MISCELLANEOUS', 'Miscellaneous')], max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='XenoType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=12)),
                ('vanilla', models.BooleanField(default=False)),
                ('carrier_type', models.IntegerField(choices=[(1, 'Endogene'), (2, 'Xenogene')])),
            ],
        ),
    ]
