# Generated by Django 4.2 on 2023-04-10 13:35

from django.db import migrations, models
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_delete_productimageadmin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productimage',
            name='path',
        ),
        migrations.AlterField(
            model_name='productimage',
            name='upload',
            field=models.ImageField(),
        ),
    ]