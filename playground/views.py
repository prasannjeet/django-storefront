from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
# A view function is one that takes a request and returns a response
# Request handler
# Action

# First create a view (or a view function), then map this view to a URL.
def say_hello(request):
    return HttpResponse('Hello World')


def get_hello(request):
    return render(request, 'hello.html', {'name': 'Prasannjeet'})
