from django.shortcuts import render

from go.datasets.census_rent import process

def index(request):
    context = {'data': process.getsomething()}
    return render(request, 'go/index.html', context)
