from defapp.views import index as defappindex
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView

urlpatterns = [
    # path("api/", include('movies.api.urls')),
    path('admin/', admin.site.urls),
    path('', defappindex, name='home'),
    path(
        'favicon.ico',
        RedirectView.as_view(url=staticfiles_storage.url('img/favicon.png')),
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
