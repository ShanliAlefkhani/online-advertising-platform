# Generated by Django 3.1.7 on 2021-04-09 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_management', '0003_auto_20210405_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='click',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='view',
            name='ip',
            field=models.GenericIPAddressField(),
        ),
    ]