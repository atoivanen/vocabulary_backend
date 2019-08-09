from django.shortcuts import render


def index(request):
    return render(request, 'build/index.html')

def en(request):
    return render(request, 'build/locales/en/translation.json')

def fi(request):
    return render(request, 'build/locales/fi/translation.json')
