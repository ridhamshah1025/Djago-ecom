# Generated by Django 3.0.2 on 2020-07-01 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(),
        ),
    ]