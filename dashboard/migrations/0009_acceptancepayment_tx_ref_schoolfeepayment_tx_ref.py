# Generated by Django 5.2.1 on 2025-06-19 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_acceptancepayment_schoolfeepayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptancepayment',
            name='tx_ref',
            field=models.CharField(default='123', max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='schoolfeepayment',
            name='tx_ref',
            field=models.CharField(default='123', max_length=100, unique=True),
        ),
    ]
