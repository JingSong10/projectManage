from django import forms
from django.core.exceptions import ValidationError

from web import models
from web.forms.bootstrap import BootStrapForm
from web.forms.widgets import ColorRadioSelect


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ['color']
    # desc = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {      # 重写属性
            'desc': forms.Textarea,
            'color': ColorRadioSelect(attrs={'class': 'color-radio'})
        }

    def clean_name(self):
        '''项目校验'''
        name = self.cleaned_data['name']
        # 当前用户是否已创建此项目
        exists = models.Project.objects.filter(name=name, creator=self.request.user_obj).exists()
        if exists:
            raise ValidationError('项目名已存在')
        # 当前用户项目额度

        count = models.Project.objects.filter(creator=self.request.user_obj).count()
        if count >= self.request.price_policy.project_num: # 最多创建项目数
            raise ValidationError('项目个数超限，请购买更多额度')
        return name


    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request