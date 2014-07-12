from django.shortcuts import render

from go.datasets.lga_suburb_list import process
from go.datasets.census_rent.process import getMedianWeeklyRent

def index(request):
    westernSydneyLGAs = ['Auburn', 'Bankstown', 'Blacktown', 'Blue Mountains', 'Camden', 'Campbelltown', 'Fairfield', 'Hawkesbury', 'Hills Shire', 'Holroyd', 'Liverpool', 'Parramatta', 'Penrith', 'Wollondilly']
    context = {}
    suburbsToLGA, lgaToRegion = process.process()
    compare = ' '.join(w.capitalize() for w in request.GET.get('compare', '').strip().split())    # trim and title capitalise

    nwss = sorted([suburb for suburb in suburbsToLGA.keys() for lga in suburbsToLGA[suburb] if lga not in westernSydneyLGAs])
    context['non_ws_suburbs'] = str(getUniqueItems(nwss)).replace("'", '"')
    context['compare'] = compare
    context['info'] = getcompareinfo(compare, suburbsToLGA, lgaToRegion, westernSydneyLGAs)
    context['medianrent'] = getMedianRent(compare, findMatchingLGAs(compare, suburbsToLGA, lgaToRegion), westernSydneyLGAs)
    return render(request, 'go/index.html', context)

def getUniqueItems(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]


def findMatchingLGAs(compare, suburbToLGA, lgaToRegion):
    if compare in lgaToRegion:
        return [compare]
    elif compare in suburbToLGA:
        return suburbToLGA[compare]
    return []

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

def getMedianRent(compare, LGAs, westernSydneyLGAs):
    medianRent = getMedianWeeklyRent(LGAs)
    medianRentWest = getMedianWeeklyRent(westernSydneyLGAs)
    if medianRent is None or medianRentWest is None:
        return ''
    out = 'The median weekly rent for Western Sydney is $' + str(medianRentWest) +\
          ', compared to $' + str(medianRent) + ' in ' + compare + '.'
    if medianRentWest < medianRent:
        out += ' That\'s an annual saving of $' + str((medianRent - medianRentWest) * 52) + '!'
    return out