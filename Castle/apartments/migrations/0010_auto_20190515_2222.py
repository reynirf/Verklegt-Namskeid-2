# Generated by Django 2.2.1 on 2019-05-15 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0009_apartment_sold'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='description',
            field=models.TextField(max_length=999),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='rooms',
            field=models.CharField(max_length=2),
        ),
    ]
