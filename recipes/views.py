from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request, "recipes/home.html", 
                context={'name': 'Vinicius'}, status=201)

def contato(request):
    return render(request, 'global/contact.html')

def sobre(request): return HttpResponse('SOBRE!')

