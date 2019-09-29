from kingadmin import app_setup

#程序一启动就执行
app_setup.kingadmin_auto_discover()

from kingadmin.sites import site
print('site',site.enable_admins)

print("------kingadmin discover printed end ------")

from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def acc_login(request):
    error_msg=''
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')

        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(request.GET.get('next','/kingadmin/'))
        else:
            error_msg ='用户名或密码错误'
    return render(request, 'kingadmin/login.html',{'error_msg':error_msg})

def acc_logout(request):
    logout(request)
    return redirect('/kingadmin/login/')

def app_index(request):
    return render(request,'kingadmin/app_index.html', {'site':site})

def get_filter_result(request,querysets):
    '''过滤结果'''
    filter_conditions ={}
    for key,val in request.GET.items():
        if key in ('page', '_o','_q'):continue
        if val:
            filter_conditions[key] = val
    return querysets.filter(**filter_conditions), filter_conditions

from django.db.models import Q

def get_searched_result(request, querysets,admin_class):
    '''搜索'''
    search_key = request.GET.get('_q')
    if search_key:
        q=Q()
        q.connector = 'OR'
        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains"%search_field,search_key))

        return querysets.filter(q)
    return querysets, search_key

def get_orderby_result(request, querysets, admin_class):
    '''排序'''
    current_ordered_column ={}
    orderby_index = request.GET.get('_o')
    if orderby_index:
        orderby_key = admin_class.list_display[abs(int(orderby_index))]
        current_ordered_column[orderby_key] = orderby_index
        if orderby_index.startswith('-'):
            orderby_key = '-' + orderby_key
        return  querysets.order_by(orderby_key), current_ordered_column
    else:
        return querysets, current_ordered_column

@login_required
def table_obj_list(request,app_name,model_name):
    admin_class = site.enable_admins[app_name][model_name]
    querysets = admin_class.model.objects.all().order_by('-id') #新增加的数据在前面
    querysets,filter_conditions = get_filter_result(request, querysets)
    admin_class.filter_conditions = filter_conditions #记录选中的值
    #搜索
    querysets, search_key = get_searched_result(request,querysets,admin_class)
    admin_class.search_key = search_key
    querysets, sorted_column = get_orderby_result(request, querysets, admin_class)

    #分页
    paginator = Paginator(querysets,2)
    page = request.GET.get('page')
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        querysets = paginator.page(1)
    except EmptyPage:
        querysets = paginator.page(paginator.num_pages)

    return render(request,'kingadmin/table_obj_list.html',{
        'querysets':querysets,
        'admin_class':admin_class,
        'sorted_column':sorted_column})

from kingadmin import form_handle
@login_required
def table_obj_change(request, app_name,model_name, pk):
    '''kingadmin 数据修改页'''
    admin_class = site.enable_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class)
    #实例化
    obj = admin_class.model.objects.get(pk=pk)
    if request.method == 'GET':
        form_obj = model_form(instance=obj)
    elif request.method == 'POST':
        form_obj = model_form(instance=obj,data =request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return  redirect("/kingadmin/%s/%s"%(app_name,model_name))
    return render(request,'kingadmin/table_obj_change.html',locals())

@login_required
def table_obj_add(request, app_name, model_name):
    '''kingadmin 数据添加'''
    admin_class = site.enable_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class)
    if request.method =='GET':
        form_obj = model_form()
    if request.method == "POST":
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/kingadmin/%s/%s" % (app_name, model_name))
    return render(request, 'kingadmin/table_obj_add.html', locals())