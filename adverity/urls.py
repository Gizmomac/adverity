from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  url('', include('analytics.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
