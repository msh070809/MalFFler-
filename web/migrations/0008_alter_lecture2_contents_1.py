# Generated by Django 4.2.4 on 2023-09-26 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_delete_lecturecontent_remove_lecture2_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture2',
            name='Contents_1',
            field=models.CharField(default='제작 교육', max_length=255),
        ),
    ]
