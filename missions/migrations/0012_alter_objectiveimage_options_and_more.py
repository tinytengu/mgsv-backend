# Generated by Django 4.0.5 on 2022-06-27 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0011_alter_dialog_text_alter_fact_text_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='objectiveimage',
            options={},
        ),
        migrations.RemoveField(
            model_name='objectiveimage',
            name='order',
        ),
    ]
