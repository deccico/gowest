from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'go/index.html', context)
