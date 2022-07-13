from django.urls import path

from playground import views

# URL Conf Module, or URLConf
urlpatterns = [
    path('hello/', views.say_hello),
    path('get-hello/', views.get_hello),
]
