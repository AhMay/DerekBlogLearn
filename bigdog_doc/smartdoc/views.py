from django.shortcuts import render, HttpResponse, reverse, Http404
from  django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
#from django.core import serializers
from . import models
from .forms import DocumentForm,CategoryForm,ProductForm
import json
import datetime
from django.db.models import Q

# Create your views here.
class ProductListView(ListView):
    model = models.Product

class ProductDetailView(DetailView):
    model = models.Product

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('smartdoc.add_product', raise_exception=True), name='dispatch')
class ProductCreateView(CreateView):
    model = models.Product
    form_class = ProductForm
    template_name = 'smartdoc/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('smartdoc.change_product', raise_exception=True), name='dispatch')
class ProductUpdateView(UpdateView):
    model = models.Product
    form_class = ProductForm
    template_name = 'smartdoc/form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj

class CategoryListView(ListView):
    model = models.Category

class CategoryDetailView(DetailView):
    model = models.Category

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('smartdoc.add_category', raise_exception=True), name='dispatch')
class CategoryCreateView(CreateView):
    model = models.Category
    form_class = CategoryForm
    template_name = 'smartdoc/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('smartdoc.change_category', raise_exception=True), name='dispatch')
class CategoryUpdateView(UpdateView):
    model = models.Category
    form_class = CategoryForm
    template_name = 'smartdoc/form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj
class DocumentList(ListView):
    model = models.Document

class DocumentDetailView(DetailView):
    model = models.Document

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('smartdoc.add_document', raise_exception=True), name='dispatch')
class DocumentCreateView(CreateView):
    model = models.Document
    form_class = DocumentForm
    template_name = 'smartdoc/form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.product = models.Product.objects.get(pk=self.kwargs['pkr'])
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required('smartdoc.change_document', raise_exception=True), name='dispatch')
class DocumentUpdateView(UpdateView):
    model = models.Document
    form_class = DocumentForm
    template_name = 'smartdoc/form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj

@csrf_exempt
def document_search(request):
    q = request.GET.get('q', None)
    if q:
        document_list = models.Document.objects.filter(Q(title__icontains=q) |
                                                       Q(product__name__icontains=q) |
                                                       Q(product__code__icontains=q))

        context = {'document_list': document_list}
        return render(request,'smartdoc/document_search.html', context)
    return render(request,'smartdoc/document_search.html')

@csrf_exempt
def doc_ajax_search(request):
    q= request.GET.get('q', None)
    if q:
        document_list = models.Document.objects.filter(Q(title__icontains=q) |
                                                       Q(product__name__icontains=q) |
                                                       Q(product__code__icontains=q))
        data=[]
        for document in document_list:
            data.append({"title": document.title, "product_name": document.product.name,
                         "category_name": document.category.name,
                         "format": document.doc_file.url.split('.')[-1].upper(),
                         "size": "{:.1f}KB".format(document.doc_file.size /1024),
                         "version": document.version_no, "date": document.mod_date,
                         "product_id": document.product.id, "id": document.id,
                         "url": document.doc_file.url,
                         })
        json_data = json.dumps(data, cls=MyEncoder)
        return HttpResponse(json_data)

def page_not_found(request, exception):
    return render(request, 'smartdoc/404.html', status=403)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')

        return json.JSONEncoder.default(self, obj)
