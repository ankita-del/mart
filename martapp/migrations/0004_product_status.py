# Generated by Django 3.1.5 on 2021-09-06 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('martapp', '0003_auto_20210906_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('under review', 'under review'), ('onboarded', 'onboarded')], default='', max_length=100),
        ),
    ]