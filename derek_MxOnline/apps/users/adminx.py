import xadmin
from .models import EmailVerifyRecord, Banner

from xadmin import views

#创建 xadmin的最进步管理器配置，并与view绑定
class BaseSetting(object):
    #开启主题功能
    enable_themes = True
    use_bootswatch = True

#将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView, BaseSetting)

#全局修改，固定写法
class GlobalSettings(object):
    #修改title
    site_title = "NBA后台管理界面"
    #修改footer
    site_footer = "科比公司"
    #收起菜单
    menu_style="accordion"

xadmin.site.register(views.CommAdminView, GlobalSettings)


#xadmin 中这里是继承 object, 不再是继承admin
class EmailVerifyRecordAdmin(object):
    #显示列
    list_display = ['code','email','send_type','send_time']
    #搜索的字段 (不要添加时间搜索）
    search_fields = ['code', 'email','send_type']
    #过滤
    list_filter = ['code', 'email', 'send_type', 'send_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)

class BannerAdmin(object):
    #显示列
    list_display = ['title','image','index','add_time']
    #搜索的字段 (不要添加时间搜索）
    search_fields = ['title','image','index']
    #过滤
    list_filter = ['title','image','index','add_time']

xadmin.site.register(Banner, BannerAdmin)