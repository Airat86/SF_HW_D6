from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView, TemplateView, FormView
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from .filters import PostFilter
from .forms import PostForm
from .models import Post, Category, UserCategory, PostCategory
from django.core.paginator import Paginator
from django.http import HttpResponse


class PostList(ListView):
    model = Post  # Указываем модель (сущность в таблице базы данных) которую нужно вывести
    template_name = 'flatpages/news.html' # Путь к html-фалу с инструкциями вывода пользователю этих объектов
    context_object_name = 'news'  # Указываем на имя списка, в котором лежат все объекты для html-шаблона
    queryset = Post.objects.order_by('-dateCreation')  # Переопределяем все новости от новых к старым
    paginate_by = 10
    form_class = PostForm  # добавляем форм класс, чтобы получать доступ к форме через метод POST

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['categories'] = Category.objects.all()
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса

        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetailView(DetailView):
    template_name = 'flatpages/post_detail.html'  # Путь к html-файлу с инструкциями вывода деталей модели (сущности)
    context_object_name = 'post'
    queryset = Post.objects.all()


class PostSearch(PostList):
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    queryset = Post.objects.all()
    paginate_by = 1


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'flatpages/post_create.html'
    context_object_name = 'post_create'
    permission_required = ('news.add_post',)
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'flatpages/post_update.html'
    permission_required = ('news.change_post',)
    form_class = PostForm

    def get_object(self, **kwargs):  # Вместо queryset, чтобы получить информацию о редактируемом объекте
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):  # Удаление новости
    template_name = 'flatpages/post_delete.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    success_url = '/news/'


class CategoryList(ListView):
    model = Category
    template_name = 'flatpages/subscribers.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        user_cat = list()
        for u in Category.objects.all():
            if (u.subscribe.filter(id=user.id).exists()):
                user_cat.append(u.name)
        context['user_category'] = user_cat
        return context


@login_required
def subscribe_user(request):
    user = request.user
    category = Category.objects.get(id=request.POST['id_cat'])
    if category.subscribe.filter(id=user.id).exists():
       category.subscribe.remove(user)
    else:
        category.subscribe.add(user)
    return redirect('/news/')
