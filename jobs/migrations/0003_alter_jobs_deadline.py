# Generated by Django 4.0.4 on 2022-05-14 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_alter_jobs_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobs',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]