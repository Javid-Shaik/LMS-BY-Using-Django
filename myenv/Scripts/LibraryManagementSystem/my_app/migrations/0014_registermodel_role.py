# Generated by Django 4.2.1 on 2023-05-31 05:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0013_alter_registermodel_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='registermodel',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('librarian', 'Librarian'), ('admin', 'Admin')], default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
    ]
