# Generated by Django 4.2.1 on 2023-06-01 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0021_borrowings_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='borrowings',
            old_name='borrowing_date',
            new_name='borrowed_date',
        ),
    ]
