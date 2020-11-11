# Generated by Django 3.1.2 on 2020-11-11 08:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Primitives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
            ],
            options={
                'verbose_name': '分类主表',
                'verbose_name_plural': '分类主表',
            },
        ),
        migrations.CreateModel(
            name='TypePar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
                ('par_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manage.primitives', verbose_name='主表id')),
            ],
            options={
                'verbose_name': '分类父表',
                'verbose_name_plural': '分类父表',
            },
        ),
        migrations.CreateModel(
            name='TypeChild',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
                ('par_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Manage.typechild', verbose_name='父表id')),
            ],
            options={
                'verbose_name': '分类子表',
                'verbose_name_plural': '分类子表',
            },
        ),
    ]
