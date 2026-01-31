from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.review.models import ContactUs, Review

# Register your models here.
@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('id', 'reviewer', 'title', 'product', 'rating', 'created_at')
    search_fields = ('reviewer__email', 'product__title', 'comment')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)

@admin.register(ContactUs)
class ContactUsAdmin(ModelAdmin):
    list_display = ('id', 'name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')
    ordering = ('-created_at',)