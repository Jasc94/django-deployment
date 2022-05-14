from django.urls import path, re_path
from basic_app import views

# Template tagging
app_name = 'basic_app'

urlpatterns = [
    re_path(r'^register/$', views.register, name='register'),
]