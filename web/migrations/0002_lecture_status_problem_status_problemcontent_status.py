# Generated by Django 4.2.4 on 2023-09-20 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='status',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AddField(
            model_name='problem',
            name='status',
            field=models.CharField(default=0, max_length=255),
        ),
        migrations.AddField(
            model_name='problemcontent',
            name='status',
            field=models.CharField(default=0, max_length=255),
        ),
    ]
