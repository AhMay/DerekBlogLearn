from django import conf

def kingadmin_auto_discover():
    for app_name in conf.settings.INSTALLED_APPS:
        print("[kingadmin.app_setup]-----"+app_name+"--------")
        try:
            #app中是否有kingadmin 模块
            mod = __import__('{}.kingadmin'.format(app_name)) # 要不要过滤掉kingadmin 自己？
            print(mod.kingadmin)
        except ImportError:
            pass #如果这个app没有定义kingadmin 模块就忽略