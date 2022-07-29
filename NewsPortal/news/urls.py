from django.urls import path
from .views import *

urlpatterns = [
    path('', PostList.as_view()),  # Путь на вкладку всех новостей "News"
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),  # Путь к деталям выбранной новости
    path('search/', PostSearch.as_view(), name='search'),  # Путь на вкладку "Поиск"
    path('create/', PostCreateView.as_view(), name='post_create'),  # Создать новость
    path('update/<int:pk>', PostUpdateView.as_view(), name='post_update'),  # Путь на редактирование новости
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),  # Удаление выбранной новости
    path('sub/', CategoryList.as_view(), name='category'),  # Путь к списку категорий с кнопками на подписку
    path('sub/subscribe/', subscribe_user, name='follow'),
    # path('sub/unsubscribe/', unfollow_user, name='unfollow'),
]
