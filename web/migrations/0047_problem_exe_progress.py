# Generated by Django 4.2.7 on 2023-12-02 07:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0046_delete_problem_exe_progress'),
    ]

    operations = [
        migrations.CreateModel(
            name='problem_exe_Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.user')),
            ],
        ),
    ]
