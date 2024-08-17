from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseForbidden
from django.conf.urls import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('expenses.urls')),
    path('', include('records.urls')),
] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static.static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def forbidden_view(request):
    return HttpResponseForbidden("Сюда нельзя")
