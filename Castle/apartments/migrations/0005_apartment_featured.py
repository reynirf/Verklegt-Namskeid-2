# Generated by Django 2.2 on 2019-05-10 02:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0004_apartment_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment_featured',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apartments.Apartment')),
            ],
        ),
    ]
