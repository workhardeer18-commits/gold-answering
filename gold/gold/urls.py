
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('OMS/', include('OMS.urls')),
    path('', include('UMS.urls')),
    ]
