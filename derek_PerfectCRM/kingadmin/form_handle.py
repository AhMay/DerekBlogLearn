#kingadmin/formhandle.py
'''
动态生成form 类
ex. def sayhi(self):
        print("你好")
    f = type('Foo',(object,),{'func':func}) #类名，当前类的基类，类的成员
    obj = f()
'''
from django.forms import ModelForm
def create_dynamic_model_form(admin_class):
    '''动态生成modelform'''
    class Meta:
        model = admin_class.model
        fields ="__all__"
        excludes = admin_class.readonly_fields

    def __new__(cls, *args,**kwargs):
        for field_name in cls.base_fields:
            field_obj = cls.base_fields[field_name]
            field_obj.widget.attrs.update({'class':'form-control'})

        return  ModelForm.__new__(cls)

    dynamic_form = type('DynamicModelForm',(ModelForm,),{'Meta':Meta,'__new__':__new__})

    return dynamic_form