# Generated by Django 4.0.3 on 2022-04-20 09:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_tmp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tmp',
        ),
    ]