import re

from django.conf import settings
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, re_path
from django.views import static

from http_stubs import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Redirect from the main page to the admin
    path('', lambda *args, **kwargs: redirect('/admin/', permanent=True)),
]

# Serve static files using Django
urlpatterns += [re_path(
    f'^{re.escape(settings.STATIC_URL.lstrip("/"))}(?P<path>.*)$',
    view=static.serve,
    kwargs={'document_root': settings.STATIC_ROOT},
)]

# Rest of the urls
urlpatterns += [
    path('<path:path>', views.HTTPStubView.as_view()),
]
