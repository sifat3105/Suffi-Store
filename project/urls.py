from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.authentication.urls')),
    path('api/', include('apps.product.urls')),
    path('api/', include('apps.favorite.urls')),
    path('api/', include('apps.cart.urls')),
    path('api/', include('apps.address.urls')),
    path('api/', include('apps.user.urls')),
    path('api/', include('apps.checkout.urls')),
    path('api/', include('apps.review.urls')),
    path('api/', include('apps.ai_chat.urls')),

    path('api/', include('apps.order.urls')),

    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)