# Generated by Django 3.1.3 on 2020-11-20 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_auto_20201116_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permission',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
