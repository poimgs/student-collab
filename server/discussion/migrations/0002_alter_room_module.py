# Generated by Django 4.0.1 on 2022-01-24 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('discussion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='module',
            field=models.CharField(max_length=255),
        ),
    ]
