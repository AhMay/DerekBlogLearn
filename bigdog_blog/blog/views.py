from django.shortcuts import render, HttpResponse, Http404, get_object_or_404, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView,DeleteView,CreateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from .forms import ArticleForm

from . import models
# Create your views here.

class ArticleListView(ListView):
    paginate_by = 3

    def get_queryset(self):
        return models.Article.objects.filter(status='p').order_by('-pub_date')

class ArticleDetailView(DetailView):
    model = models.Article
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.viewed()
        return obj

@method_decorator(login_required,name='dispatch')
class ArticleCreateView(CreateView):
    model = models.Article
    form_class = ArticleForm
    template_name = 'blog/article_create_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form)

@method_decorator(login_required,name='dispatch')
class ArticleUpdateView(UpdateView):
    model = models.Article
    form_class = ArticleForm
    template_name ='blog/article_create_form.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj

@method_decorator(login_required, name='dispatch')
class ArticleDeleteView(DeleteView):
    model = models.Article
    success_url = reverse_lazy('blog:article_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        if obj.author != self.request.user:
            raise Http404()
        return obj

@method_decorator(login_required, name='dispatch')
class PublishedArticleListView(ListView):
    paginate_by = 3
    template_name = 'blog/published_article_list.html'

    def get_queryset(self):
        return models.Article.objects.filter(author=self.request.user)\
                .filter(status='p').order_by('-pub_date')

@method_decorator(login_required, name='dispatch')
class ArticleDraftListView(ListView):
    paginate_by = 3
    template_name = 'blog/article_draft_list.html'

    def get_queryset(self):
        return models.Article.objects.filter(author=self.request.user) \
            .filter(status='d').order_by('-pub_date')

class CategoryListView(ListView):
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        return models.Category.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topping'] = [category for category in context['category_list'] if category.parent_category is None]
        return context

class CategoryDetailView(ListView):
    paginate_by = 3
    template_name = 'blog/article_list.html'
    def get_queryset(self):
        category_id = self.kwargs['pk']
        return models.Article.objects.filter(category__id=category_id).filter(status='p').order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        context['category'] = models.Category.objects.get(pk=category_id)
        return context

class TagDetailView(ListView):
    paginate_by = 3
    template_name = 'blog/article_list.html'
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        print(tag_slug)
        return models.Article.objects.filter(tags__slug=tag_slug).filter(status='p').order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs['slug']
        context['tags'] = models.Tag.objects.get(slug=tag_slug)
        return context

@login_required
def article_publish(request, pk, slug):
    article = get_object_or_404(models.Article,pk=pk,author=request.user)
    article.published()
    return  redirect('blog:article_detial', args=[pk,slug])

def article_search(request):
    return HttpResponse("article_search")

@login_required
@require_http_methods(["POST"])
def article_like(request):
    article_id = request.POST.get('id')
    action = request.POST.get('action')
    if article_id and action:
        try:
            article = models.Article.objects.get(id=article_id)
            if action == 'like':
                article.users_like.add(request.user)
            else:
                article.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'fail'})

