from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('accounts/signup', views.signup, name='signup'),
]


#class based views expect <int:pk>
#function based views expect <int:model_id>
#djangoauth doesnt have signup urls

