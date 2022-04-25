from django.db import models

from interfaces.models import Interfaces
from utils.base_models import BaseModel


class TestCases(BaseModel):
    objects = None
    id = models.AutoField(verbose_name='id主键', help_text='id主键', primary_key=True)
    name = models.CharField(verbose_name='用例名称', help_text='用例名称', unique=True, max_length=50)
    include = models.TextField(verbose_name='前置顺序', null=True, help_text='前置顺序')
    author = models.CharField(verbose_name='编写人员', max_length=50, help_text='编写人员')
    request = models.TextField(verbose_name='请求信息', help_text='请求信息')
    interface = models.ForeignKey(Interfaces, on_delete=models.CASCADE, related_name='testcases', help_text='所属接口')

    class Meta:
        db_table = 'tb_testcases'
        verbose_name = '用例信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
