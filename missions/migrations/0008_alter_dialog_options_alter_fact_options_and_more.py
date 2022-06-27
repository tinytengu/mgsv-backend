# Generated by Django 4.0.5 on 2022-06-27 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('missions', '0007_alter_objective_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dialog',
            options={'verbose_name': 'Dialog', 'verbose_name_plural': 'Dialogs'},
        ),
        migrations.AlterModelOptions(
            name='fact',
            options={'verbose_name': 'Fact', 'verbose_name_plural': 'Facts'},
        ),
        migrations.AlterModelOptions(
            name='mission',
            options={'verbose_name': 'Mission', 'verbose_name_plural': 'Missions'},
        ),
        migrations.AlterField(
            model_name='mission',
            name='chapter',
            field=models.IntegerField(default=1, verbose_name='chapter'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='number',
            field=models.IntegerField(default=0, verbose_name='number'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='type',
            field=models.IntegerField(choices=[(0, 'Default'), (1, 'Flashback'), (2, 'Autonomy'), (3, 'Stealth')], default=0, verbose_name='type'),
        ),
    ]
