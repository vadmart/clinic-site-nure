# Generated by Django 4.1.7 on 2023-04-17 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_remove_review_commentator_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='lastname_en',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='lastname_uk',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='name_en',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='name_uk',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='patronymic_en',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='patronymic_uk',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='doctor',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='doctorcategory',
            name='name_en',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='doctorcategory',
            name='name_uk',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='cabinet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.cabinet'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.patient'),
        ),
    ]
