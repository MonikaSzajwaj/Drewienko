# Generated by Django 3.1.3 on 2020-11-21 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_auto_20201121_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('szafy', 'szafy'), ('komody', 'komody'), ('sofy', 'sofy'), ('zestawy wypoczynkowe', 'zestawy wypoczynkowe'), ('meblościanki', 'meblościanki'), ('ławy i stoliki', 'ławy i stoliki'), ('krzesła', 'krzesła')], max_length=150, verbose_name='Kategoria'),
        ),
    ]
