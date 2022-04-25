from django.db import models
from utils.base_models import BaseModel


class TestPlans(BaseModel):
    name = models.CharField(verbose_name='计划名称', help_text='计划名称', max_length=200)
    structure_time = models.CharField(help_text='构建时间', max_length=100, verbose_name='构建时间')
    env_id = models.IntegerField(help_text='环境id', verbose_name='环境id')

    # user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建人员', help_text='创建人员')

    class Meta:
        db_table = 'tb_testplans'
        verbose_name = '测试计划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
