from django.shortcuts import render

from go.datasets.lga_suburb_list import process

def index(request):
    context = {}
    suburbsToLGA, lgaToRegion = process.process()
    try:
        compareu = request.GET.get('compare', '')
        context['compare'] = ' '.join(w.capitalize() for w in compareu.encode('utf8').strip().split())    # trim and title capitalise
    except UnicodeDecodeError:
        context['compare'] = ''
    context['info'] = getcompareinfo(context['compare'], suburbsToLGA, lgaToRegion)
    return render(request, 'go/index.html', context)

def getcompareinfo(compare, suburbToLGA, lgaToRegion):
    if compare == '':
        return ''

    out = compare + ' is a '

    type = None
    lgaStr = ''
    region = ''
    if compare in suburbToLGA:
        type = 'suburb'
        lgas = suburbToLGA[compare]
        lgaStr = ' in the local government area'
        if len(lgas) == 1:
            lgaStr += ' of ' + lgas[0]
        else:
            lgaStr += 's of ' + ', '.join(lgas[:-1]) + ' and ' + lgas[-1]
        lgaStr += ','
        region = lgaToRegion[lgas[0]]
    elif compare in lgaToRegion:
        type = 'local government area'
        region = lgaToRegion[compare]
    if type is None:
        return ''

    out += type + lgaStr + ' in the ' + region + ' region.'

    return out