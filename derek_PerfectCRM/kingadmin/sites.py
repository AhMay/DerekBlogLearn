#kingadmin/sites
from kingadmin.admin_base import BaseKingAdmin
class AdminSite(object):
    def __init__(self):
        self.enable_admins ={} #存放 app, model_name 以及 admin_class

    #两个参数，一个表名，一个自定义的admin类
    def register(self, model_class, admin_class=None):
        '''注册admin表'''
        app_name = model_class._meta.app_label #获取app name
        model_name = model_class._meta.model_name  #获取表名
        if admin_class is None:
            admin_class = BaseKingAdmin() #变成实例
        else:
            admin_class = admin_class() #变成实例
        admin_class.model = model_class #将 admin_class 和它的 model 类 关联起来,如果没有定义，则默认为BaseKingAdmin

        if app_name not in self.enable_admins:
            self.enable_admins[app_name] = {}

        self.enable_admins[app_name][model_name] = admin_class

site = AdminSite()