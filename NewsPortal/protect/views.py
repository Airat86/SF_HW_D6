from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class MyView(PermissionRequiredMixin, View):
    permission_required = ('news.create_post',
                           'news.delete_post')


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context
