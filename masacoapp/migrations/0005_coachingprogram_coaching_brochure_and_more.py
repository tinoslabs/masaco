# Generated by Django 5.1.4 on 2025-05-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masacoapp', '0004_coachingprogram_delete_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='coachingprogram',
            name='coaching_brochure',
            field=models.FileField(blank=True, null=True, upload_to='course_brochures/'),
        ),
        migrations.AddField(
            model_name='coachingprogram',
            name='coaching_deatils',
            field=models.TextField(blank=True, null=True),
        ),
    ]
