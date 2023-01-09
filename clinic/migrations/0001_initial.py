# Generated by Django 4.1.5 on 2023-01-07 23:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cabinets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Doctors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('lastname', models.CharField(max_length=30)),
                ('patronymic', models.CharField(max_length=20)),
                ('work_start_date', models.DateField()),
                ('category_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.doctorcategories')),
            ],
        ),
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15)),
                ('lastname', models.CharField(max_length=30)),
                ('contract_num', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=12)),
                ('street_type', models.CharField(max_length=10)),
                ('street_name', models.CharField(max_length=40)),
                ('house_number', models.CharField(max_length=4)),
                ('flat_number', models.CharField(max_length=4)),
                ('post_index', models.IntegerField()),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.doctors')),
            ],
        ),
        migrations.CreateModel(
            name='WeekDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=9)),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2023, 1, 7, 23, 49, 46, 504252, tzinfo=datetime.timezone.utc))),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.doctors')),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.persons')),
            ],
        ),
        migrations.CreateModel(
            name='Recordings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('health_complaint', models.CharField(max_length=255)),
                ('was_patient_present', models.BooleanField(default=False)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.doctors')),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.persons')),
            ],
        ),
        migrations.CreateModel(
            name='PhoneNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=12)),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.doctors')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorWorkingSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.doctors')),
                ('week_day_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.weekdays')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorsCabinets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cabinet_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.cabinets')),
                ('doctor_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic.doctors')),
            ],
        ),
        migrations.AddConstraint(
            model_name='doctorworkingschedule',
            constraint=models.UniqueConstraint(fields=('doctor_id', 'week_day_id'), name='pk_doctor_working_schedule'),
        ),
    ]
