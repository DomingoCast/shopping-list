# Generated by Django 3.0.6 on 2020-05-23 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listapp', '0002_auto_20200523_1213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='familia',
            name='miembro',
        ),
        migrations.AddField(
            model_name='familia',
            name='miembro',
            field=models.ManyToManyField(to='listapp.Customer'),
        ),
    ]
