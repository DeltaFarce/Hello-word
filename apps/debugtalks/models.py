from django.db import models

from projects.models import Projects
from utils.base_models import BaseModel


class Debugtalks(BaseModel):
    objects = None
    id = models.AutoField(verbose_name="Id主键", primary_key=True, help_text="Id主键")
    name = models.CharField(verbose_name="debugtalk文件名称", max_length=200, help_text="debugtalk文件名称")
    debugtalk = models.TextField(verbose_name="debugtalk文件", null=True, default="#debugtalk.py", help_text="debugtalk文件")
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name="debugtalks", help_text="所属项目")

    class Meta:
        db_table = 'tb_bebugtalks'
        verbose_name = 'debugtalk文件'
        verbose_name_plural = 'debugtalk文件'

    def __str__(self):
        return self.name
