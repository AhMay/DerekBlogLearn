import datetime

from django.template import Library
from django.utils.safestring import mark_safe

register = Library()

@register.simple_tag
def build_table_row(obj,admin_class):
    '''生成一条记录的html element'''
    ele=''
    if admin_class.list_display:
        for index, column_name in enumerate(admin_class.list_display):
            column_obj = admin_class.model._meta.get_field(column_name)
            if column_obj.choices:
                column_data = getattr(obj, 'get_{}_display'.format(column_name))
            else:
                column_data = getattr(obj, column_name)
            td_ele = "<td>{}</td>".format(column_data)
            if index ==0:
                td_ele = "<td><a href='%s/change/'>%s</a></td>"%(obj.id, column_data) #给第一列添加一个锚,点击可以修改
            ele+=td_ele
    else:
        #td_ele = "<td>%s</td>"%obj
        td_ele = "<td><a href='%s/change/'>%s</a></td>" % (obj.id, obj)
    return mark_safe(ele)

#添加过滤功能
@register.simple_tag
def build_filter_ele(filter_column,admin_class):
    column_obj = admin_class.model._meta.get_field(filter_column)
    try:
        filter_ele = "<div class='col-md-2'>{}<select class='form-control' name='{}'>".format(filter_column,filter_column)
        for choice in column_obj.get_choices():
            selected =''
            if filter_column in admin_class.filter_conditions:
                if str(choice[0]) == admin_class.filter_conditions.get(filter_column):
                    selected='selected'
            option = "<option value='%s' %s>%s</option>"%(choice[0], selected,choice[1])
            filter_ele +=option
    except AttributeError as e:
        filter_ele = "<div class='col-md-2'>{}<select class='form-control' name='{}__gte'>".format(filter_column,filter_column)
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            time_obj = datetime.datetime.now()
            time_list =[
                ['','-------'],
                [time_obj,'Today'],
                [time_obj - datetime.timedelta(days=7),'七天内'],
                [time_obj.replace(day=1),'本月'],
                [time_obj- datetime.timedelta(days=90), '三个月内'],
                [time_obj.replace(month=1,day=1),'YearToDay(YTD)'],
            ]
            for i in time_list:
                selected=''
                time_to_str = '' if not i[0] else "%s-%s-%s"%(i[0].year, i[0].month, i[0].day)
                if "%s__gte"%filter_column in admin_class.filter_conditions:
                    if time_to_str == admin_class.filter_conditions.get("%s__gte"%filter_column):
                        selected ='selected'
                option = "<option value='%s' %s>%s</option>"%(time_to_str,selected, i[1])
                filter_ele += option
    filter_ele +="<select/></div>"

    return  mark_safe(filter_ele)

@register.simple_tag
def get_model_name(admin_class):
    '''获取表名'''
    return admin_class.model._meta.model_name.upper()

@register.simple_tag
def render_paginator(querysets, admin_class, sorted_column):
    '''分页'''
    ele = '''<ul class="pagination"> '''
    for i in querysets.paginator.page_range:
        # 显示前后三页，abs是绝对值
        if abs(querysets.number - i) < 3:
            active =''
            if querysets.number == i:
                active ='active'
            #组合过滤字段
            filter_ele = render_filtered_args(admin_class)
            #排序字段
            sorted_ele=''
            if sorted_column:
                sorted_ele = '&_o=%s'%list(sorted_column.values())[0]
            p_ele = '''<li class='%s'><a href='?page=%s%s%s'>%s</a></li>'''%(active, i, filter_ele,sorted_ele, i)

            ele += p_ele

    ele += "</ul>"
    return  mark_safe(ele)

@register.simple_tag
def get_sorted_column(column, sorted_column, forloop):
    '''排序'''
    if column in sorted_column:
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            this_time_sort_index = last_sort_index.strip('-')
        else:
            this_time_sort_index = '-'+last_sort_index
        return this_time_sort_index
    else:
        return forloop

@register.simple_tag
def render_sorted_arrow(column,sorted_column):
    '''排序的图标'''
    if column in sorted_column:
        last_sort_index = sorted_column[column]
        if last_sort_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction ='top'

        ele = '''<span class='glyphicon glyphicon-triangle-%s' aria-hidden='true'></span> '''% arrow_direction
        return mark_safe(ele)

    return ''

@register.simple_tag
def render_filtered_args(admin_class, render_html=True): #不能让一排序就把过滤条件给丢掉了
    '''拼接过滤的字段'''
    if admin_class.filter_conditions:
        ele=''
        for k, v in admin_class.filter_conditions.items():
            ele +='&%s=%s'%(k,v)
        if render_html:
            return mark_safe(ele)
        else:
            return ele
    else:
        return ''

@register.simple_tag
def get_current_sorted_column_index(sorted_column):
    return list(sorted_column.values())[0] if sorted_column else ''

@register.simple_tag
def get_obj_field_val(form_obj,field):
    '''获取只读字段的值'''
    return getattr(form_obj.instance, field)