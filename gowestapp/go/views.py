from django.shortcuts import render

from go.datasets.lga_suburb_list import process

def index(request):
    westernSydneyLGAs = ['Auburn', 'Bankstown', 'Blacktown', 'Blue Mountains', 'Camden', 'Campbelltown', 'Fairfield', 'Hawkesbury', 'Hills Shire', 'Holroyd', 'Liverpool', 'Parramatta', 'Penrith', 'Wollondilly']
    context = {}
    suburbsToLGA, lgaToRegion = process.process()
    try:
        compareu = request.GET.get('compare', '')
        context['compare'] = ' '.join(w.capitalize() for w in compareu.encode('utf8').strip().split())    # trim and title capitalise
    except UnicodeDecodeError:
        context['compare'] = ''
    context['info'] = getcompareinfo(context['compare'], suburbsToLGA, lgaToRegion, westernSydneyLGAs)
    return render(request, 'go/index.html', context)

def getcompareinfo(compare, suburbToLGA, lgaToRegion, westernSydneyLGAs):
    if compare == '':
        return ''

    out = compare + ' is a '

    type = None
    lgas = []
    lgaStr = ''
    region = ''
    if compare in lgaToRegion and compare in suburbToLGA:
        type = 'suburb and local government area'
        lgas = [compare]
        region = lgaToRegion[compare]
    elif compare in lgaToRegion:
        type = 'local government area'
        lgas = [compare]
        region = lgaToRegion[compare]
    elif compare in suburbToLGA:
        type = 'suburb'
        lgas = suburbToLGA[compare]
        lgaStr = ' in the local government area'
        if len(lgas) == 1:
            lgaStr += ' of ' + lgas[0]
        else:
            lgaStr += 's of ' + ', '.join(lgas[:-1]) + ' and ' + lgas[-1]
        lgaStr += ','
        region = lgaToRegion[lgas[0]]
    if type is None:
        return ''

    out += type + lgaStr + ' in the ' + region + ' region.'

    if len(lgas) > 0 and lgas[0] in westernSydneyLGAs:
        out += ' It is part of Western Sydney!'

    return out