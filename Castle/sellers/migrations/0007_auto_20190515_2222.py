# Generated by Django 2.2.1 on 2019-05-15 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0006_auto_20190514_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seller',
            name='description',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]