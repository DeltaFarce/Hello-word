from django.db import models

from projects.models import Projects
from utils.base_models import BaseModel


class TestSuits(BaseModel):
    objects = None
    id = models.AutoField(verbose_name="ID主键", help_text='ID主键', primary_key=True)
    name = models.CharField(verbose_name='套件名称', help_text='套件名称', max_length=200, unique=True)
    include = models.TextField(verbose_name='包含接口', null=True, help_text='包含接口')
    project = models.ForeignKey(Projects, on_delete=models.CASCADE, related_name='testsuit', help_text='所属项目')

    class Meta:
        db_table = 'tb_testsuit'
        verbose_name = '套件信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
