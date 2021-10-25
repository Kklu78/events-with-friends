from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.index, name='index'),
    path('events/search/', views.search, name='search'),
    path('events/<slug:event_id>/', views.details, name='details'),
    path('events/<slug:event_id>/add_event/', views.add_event, name='add_event'),
    path('accounts/signup/', views.signup, name='signup'),


]


#class based views expect <int:pk>
#function based views expect <int:model_id>
#djangoauth doesnt have signup urls

