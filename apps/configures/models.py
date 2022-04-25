from django.db import models
from utils.base_models import BaseModel
from interfaces.models import Interfaces


class Configures(BaseModel):
    objects = None
    id = models.AutoField(verbose_name="Id主键", help_text="Id主键", primary_key=True)
    name = models.CharField(verbose_name="配置名称", max_length=200, help_text='配置名称')
    author = models.CharField(verbose_name="作者", max_length=50, help_text="作者")
    request = models.TextField(verbose_name="请求信息", help_text="请求信息")
    interfaces = models.ForeignKey(Interfaces, on_delete=models.CASCADE, help_text='所属接口')

    class Meta:
        verbose_name = "配置信息"
        db_table = "tb_configures"
        verbose_name_plural = "配置信息"

    def __str__(self):
        return self.name
