from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import RecentlyViewedProduct, User, Account, LoginHistory, Wishlist, WishlistItem
from unfold.admin import ModelAdmin

admin.site.site_header = "Sufi's Administration"
admin.site.site_title = "Sufi's Admin"
admin.site.index_title = "Admin Dashboard"


# @admin.register(User)
class UserAdmin(ModelAdmin):
	list_display = ("email", "is_staff", "is_active", "created_at", "last_login")
	list_filter = ("is_staff", "is_active")
	search_fields = ("email",)
	ordering = ("email",)

admin.site.register(User, UserAdmin)

@admin.register(Account)
class AccountAdmin(ModelAdmin):
	list_display = ("id", "user", "name", "phone")


@admin.register(LoginHistory)
class LoginHistoryAdmin(ModelAdmin):
	list_display = ("id", "user", "device", "ip_address", "login_time")
	search_fields = ("user__email", "device")
	list_filter = ("login_time",)
	ordering = ("-login_time",)


@admin.register(Wishlist)
class WishlistAdmin(ModelAdmin):
	list_display = ("id", "user")


@admin.register(WishlistItem)
class WishlistItemAdmin(ModelAdmin):
	list_display = ("id", "wishlist", "product_id")

@admin.register(RecentlyViewedProduct)
class RecentlyViewedProductAdmin(ModelAdmin):
	list_display = ('id', 'user', 'product', 'viewed_at')
	search_fields = ('user__email', 'product__name')
	ordering = ('-viewed_at',)
