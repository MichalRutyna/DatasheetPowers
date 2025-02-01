# Generated by Django 4.2.17 on 2025-02-01 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Nation', '0013_alter_nation_pkb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='army',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='size',
            field=models.IntegerField(default=0, verbose_name='Size'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='upkeep_per_unit',
            field=models.IntegerField(default=0, verbose_name='Upkeep per unit'),
        ),
    ]
