# Generated by Django 5.1.1 on 2024-10-05 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_entrylog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EntryLog',
        ),
        migrations.RemoveField(
            model_name='tagentry',
            name='people_count',
        ),
    ]
