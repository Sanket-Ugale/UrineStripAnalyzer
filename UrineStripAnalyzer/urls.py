from django.contrib import admin
from django.urls import path, include
import strip_analyzer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('strip_analyzer.urls')),
]
