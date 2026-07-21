from django.urls import path

from . import views

urlpatterns = [
    path('', views.component_list, name='list'),
    path('<int:pk>/', views.component_detail, name='detail'),
]
