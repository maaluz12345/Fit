# Generated by Django 4.0 on 2024-04-10 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('earring_app', '0006_alter_customerprofile_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='username',
            field=models.CharField(editable=False, max_length=150, unique=True),
        ),
    ]
