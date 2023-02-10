from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.login, name="login"),
    path("main", views.main, name="main"),
    path("deleteall", views.deleteall, name="deleteall"),
    path('get_data/', views.get_data, name='get_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)