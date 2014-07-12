from django.shortcuts import render

from datasets.census_rent import process
def index(request):
    context = {}
    return render(request, 'go/index.html', context)
