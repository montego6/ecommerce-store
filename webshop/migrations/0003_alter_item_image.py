# Generated by Django 4.0.4 on 2022-06-09 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webshop', '0002_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads'),
        ),
    ]
