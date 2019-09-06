from django import forms
from . import models

class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        exclude = ['author','create_date','mod_date']
        widgets ={
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels ={
            'name': '产品名称',
            'code': '产品代码',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        exclude = ['author','create_date','mod_date']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'name': '类别',
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.Document
        exclude = ['author','create_date','mod_date','product']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'version_no': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'doc_file': forms.FileInput(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': "文档标题",
            'version_no': "版本号",
            'category':"文档类别",
            'doc_file': "上传文件",
        }