# Generated by Django 3.1.5 on 2021-09-06 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('martapp', '0006_auto_20210906_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproduct',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
