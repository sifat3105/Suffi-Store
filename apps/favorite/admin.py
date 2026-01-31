from django.contrib import admin
from apps.favorite.models import Favorite
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('id', 'user', 'product', 'created_at')
    search_fields = ('user__email', 'product__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    list_select_related = ('user', 'product')