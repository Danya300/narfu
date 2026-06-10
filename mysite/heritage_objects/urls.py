from django.urls import path
from . import views

app_name = 'heritage_objects'

urlpatterns = [
    path('', views.heritage_object_list, name='heritage_object_list'),
    path('<int:pk>/', views.heritage_object_detail, name='heritage_object_detail'),
]