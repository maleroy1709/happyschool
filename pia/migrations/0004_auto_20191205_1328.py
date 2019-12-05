# Generated by Django 2.2.8 on 2019-12-05 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pia', '0003_auto_20191205_1118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assessmentmodel',
            name='branches',
        ),
        migrations.RemoveField(
            model_name='assessmentmodel',
            name='cross_goals',
        ),
        migrations.AlterField(
            model_name='assessmentmodel',
            name='assessment',
            field=models.CharField(help_text="Description de l'évaluation.", max_length=200),
        ),
    ]