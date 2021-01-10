# Generated by Django 3.1.3 on 2021-01-09 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_usermood_star_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='LifePer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='User.user')),
            ],
            options={
                'verbose_name': '生活部',
                'verbose_name_plural': '生活部',
                'db_table': '',
                'managed': True,
            },
        ),
    ]
