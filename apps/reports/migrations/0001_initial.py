# Generated by Django 3.2.3 on 2021-08-03 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('create_time', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, help_text='逻辑删除', verbose_name='逻辑删除')),
                ('id', models.AutoField(help_text='id主键', primary_key=True, serialize=False, verbose_name='id主键')),
                ('name', models.CharField(help_text='报告名称', max_length=200, unique=True, verbose_name='报告名称')),
                ('result', models.BooleanField(default=1, help_text='执行结果', verbose_name='执行结果')),
                ('count', models.IntegerField(help_text='用例总数', verbose_name='用例总数')),
                ('success', models.IntegerField(help_text='成功总数', verbose_name='成功总数')),
                ('html', models.TextField(blank=True, help_text='报告HTML源码', null=True, verbose_name='报告HTML源码')),
                ('summary', models.TextField(blank=True, default='', help_text='报告详情', null=True, verbose_name='报告详情')),
            ],
            options={
                'verbose_name': '测试报告',
                'verbose_name_plural': '测试报告',
                'db_table': 'tb_report',
            },
        ),
    ]
