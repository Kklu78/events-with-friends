from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.index, name='index'),
    path('events/search/', views.search, name='search'),
    path('events/<slug:event_id>/', views.details, name='details'),
    path('events/<slug:event_id>/add_event/', views.add_event, name='add_event'),
    path('events/<slug:event_id>/remove_event/', views.remove_event, name='remove_event'),
    path('accounts/signup/', views.signup, name='signup'),
    path('events/<slug:event_id>/add_comment/', views.add_comment, name='add_comment'),
    path('events/<slug:event_id>/<int:comment_id>/delete_comment/', views.delete_comment, name='delete_comment'),


]


#class based views expect <int:pk>
#function based views expect <int:model_id>
#djangoauth doesnt have signup urls

