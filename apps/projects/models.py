from utils.base_models import BaseModel
from django.db import models


class Projects(BaseModel):
    objects = None
    id = models.AutoField(verbose_name="Id主键", primary_key=True, help_text="Id主键")
    name = models.CharField(verbose_name="项目名称", max_length=200, unique=True, help_text="项目名称")
    leader = models.CharField(verbose_name="负责人", max_length=200, help_text="负责人")
    tester = models.CharField(verbose_name="测试人", max_length=200, help_text="测试人")
    programer = models.CharField(verbose_name="开发人", max_length=200, help_text="开发人")
    publish_app = models.CharField(verbose_name="发布应用", max_length=200, help_text="发布应用")
    desc = models.TextField(verbose_name="描述", help_text="描述", blank=True, default='', null=True)

    class Meta:
        db_table = 'tb_projects'
        verbose_name = '项目信息'
        verbose_name_plural = '项目信息'

    def __str__(self):
        return self.name