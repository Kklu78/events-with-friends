from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.index, name='index'),
    path('events/details/', views.details, name='details'),
    path('search/', views.search, name='search'),


]


#class based views expect <int:pk>
#function based views expect <int:model_id>
#djangoauth doesnt have signup urls

