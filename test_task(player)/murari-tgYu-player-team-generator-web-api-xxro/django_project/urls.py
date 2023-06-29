from django.urls import path, include, re_path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include('my_app.urls')),
]
