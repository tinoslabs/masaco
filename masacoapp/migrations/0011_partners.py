# Generated by Django 5.1.4 on 2025-05-04 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masacoapp', '0010_alter_abroadstudies_country_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partners',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('logo', models.ImageField(upload_to='team_images/')),
            ],
        ),
    ]
