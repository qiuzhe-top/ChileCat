# Generated by Django 3.1.2 on 2020-11-04 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Career',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='岗位名称')),
                ('note', models.CharField(max_length=300, verbose_name='岗位介绍')),
                ('text', models.CharField(max_length=999, verbose_name='正文')),
                ('source', models.CharField(max_length=100, verbose_name='地址')),
                ('viewnum', models.IntegerField(verbose_name='浏览数')),
                ('release_time', models.TimeField(verbose_name='发布时间')),
            ],
            options={
                'verbose_name': '就业信息表',
                'verbose_name_plural': '就业信息表',
            },
        ),
    ]
