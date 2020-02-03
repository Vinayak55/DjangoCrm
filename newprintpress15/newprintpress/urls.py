from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # path('', auth_views.LoginView.as_view()),

    path('admin/', admin.site.urls),
    path('login/', include('django.contrib.auth.urls')),
    path('',include('printapp.urls')),
    path('',include('material.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)