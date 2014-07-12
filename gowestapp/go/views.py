from django.shortcuts import render

from go.datasets.lga_suburb_list import process

def index(request):
    context = {'suburbsToLGAs': process.process()}
    context['compare'] = request.GET.get('compare', '')
    return render(request, 'go/index.html', context)
