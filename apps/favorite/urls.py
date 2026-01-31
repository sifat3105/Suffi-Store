from django.urls import path
from .views import AddOrRemoveListFavoriteView

urlpatterns = [
    path('favorites/', AddOrRemoveListFavoriteView.as_view(), name='favorite-list-add-remove')
]