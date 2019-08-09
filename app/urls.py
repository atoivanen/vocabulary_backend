from django.contrib import admin
from django.urls import include, path, re_path

from app.views import index, en, fi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', index, name='index'),
    path('locales/en/translation.json', en),
    path('locales/fi/translation.json', fi),
    re_path(r'^chapters/.*', index),
    path('dictionary/', index),
    path('myvocabulary/', index),
    path('about/', index),
    path('logout/', index),
    path('register/', index),
    path('login/', index),
    path('new/', index),
    re_path(r'^edit/.*', index),
]
