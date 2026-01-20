from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # core pages
    path("", include("core.urls")),

    # auth
    path("accounts/", include("accounts.urls")),

    # modules
    path("entreprises/", include("entreprises.urls")),
    path("offres/", include("offres.urls")),
    path("candidatures/", include("candidatures.urls")),
    path("conventions/", include("conventions.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
