# Generated by Django 5.1.4 on 2025-05-03 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masacoapp', '0008_contact'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('rating', models.PositiveSmallIntegerField(default=5)),
                ('message', models.TextField()),
                ('image', models.ImageField(upload_to='testimonial_images/')),
            ],
        ),
    ]
