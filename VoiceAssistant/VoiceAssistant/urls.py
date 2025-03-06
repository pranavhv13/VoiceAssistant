
from django.contrib import admin
from django.urls import path
from VoiceAssistant.views import runcode

urlpatterns = [
    path('admin/', admin.site.urls),
    path('run/',runcode,name='runcode')
]

