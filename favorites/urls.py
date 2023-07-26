from django.urls import path, re_path

from favorites.views import FavoritesAddView, FavoritesRemoveView

urlpatterns = [
    path('add/',FavoritesAddView.as_view(),name='add'),
    path('remove/',FavoritesRemoveView.as_view(),name='remove'),
]