# Generated by Django 2.2.24 on 2022-11-04 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0004_auto_20221104_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='iin',
            field=models.CharField(default='', max_length=20),
        ),
    ]
