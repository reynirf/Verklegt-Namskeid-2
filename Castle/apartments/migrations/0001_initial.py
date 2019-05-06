# Generated by Django 2.2 on 2019-05-06 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('zip_code', models.IntegerField()),
                ('rooms', models.IntegerField()),
                ('size', models.IntegerField()),
                ('price', models.IntegerField()),
                ('description', models.CharField(max_length=999)),
                ('date_added', models.DateField()),
            ],
        ),
    ]
