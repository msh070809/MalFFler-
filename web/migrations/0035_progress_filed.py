# Generated by Django 4.2.7 on 2023-11-30 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0034_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='progress',
            name='filed',
            field=models.TextField(default='', max_length=50),
        ),
    ]
