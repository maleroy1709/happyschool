# Generated by Django 2.2.4 on 2019-08-19 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_responsiblemodel_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='LessonModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson', models.CharField(max_length=200)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ClasseModel')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='StudentLatenessTeacherModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('comment', models.TextField(blank=True)),
                ('datetime_creation', models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création de l'absence")),
                ('datetime_update', models.DateTimeField(auto_now=True, verbose_name="Date et heure de mise à jour de l'absence")),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_absence_teacher.LessonModel')),
                ('period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_absence_teacher.PeriodModel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.StudentModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudentAbsenceTeacherSettingsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teachings', models.ManyToManyField(default=None, to='core.TeachingModel')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAbsenceTeacherModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('comment', models.TextField(blank=True)),
                ('datetime_creation', models.DateTimeField(auto_now_add=True, verbose_name="Date et heure de création de l'absence")),
                ('datetime_update', models.DateTimeField(auto_now=True, verbose_name="Date et heure de mise à jour de l'absence")),
                ('lesson', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_absence_teacher.LessonModel')),
                ('period', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='student_absence_teacher.PeriodModel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.StudentModel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]