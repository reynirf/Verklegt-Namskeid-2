# Generated by Django 2.2 on 2019-05-12 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190512_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='cc_cvc',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='cc_expires',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='credit_card',
            field=models.CharField(max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='profile_pic',
            field=models.CharField(max_length=999, null=True),
        ),
    ]
