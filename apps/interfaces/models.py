from django.db import models

from projects.models import Projects
from utils.base_models import BaseModel


class Interfaces(BaseModel):
    objects = None
    id = models.AutoField(verbose_name='Id主键', primary_key=True, help_text='Id主键')
    name = models.CharField(verbose_name="接口名称", max_length=50, help_text="接口名称")
    tester = models.CharField(verbose_name="测试人员", max_length=50, help_text="测试人员")
    desc = models.TextField(verbose_name="简要描述", help_text="简要描述")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='interfaces', help_text='所属项目')

    class Meta:
        db_table = "tb_interfaces"
        verbose_name = "接口信息"
        verbose_name_plural = "接口信息"

    def __str__(self):
        return self.name
