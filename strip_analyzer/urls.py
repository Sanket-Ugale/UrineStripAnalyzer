from django.urls import path
from strip_analyzer.views import *
urlpatterns = [
    path('analyze_strip/', analyze_strip, name='analyze_strip'),
    path('', home, name='home')
]
