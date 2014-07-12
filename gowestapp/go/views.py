from django.shortcuts import render

from go.datasets.lga_suburb_list import process
from go.datasets.census_rent.process import getMedianWeeklyRent
from go.datasets.attractions.process import selectrandom2attractions
from go.datasets.events.process import selectrandom2events

def index(request):
    westernSydneyLGAs = ['Auburn', 'Bankstown', 'Blacktown', 'Blue Mountains', 'Camden', 'Campbelltown', 'Fairfield', 'Hawkesbury', 'The Hills', 'Holroyd', 'Liverpool', 'Parramatta', 'Penrith', 'Wollondilly']
    context = {}
    suburbsToLGA, lgaToRegion, suburbToPostcode = process.process()
    compare = ' '.join(w.capitalize() for w in request.GET.get('compare', '').strip().split())    # trim and title capitalise

    nwss = sorted([suburb for suburb in suburbsToLGA.keys() for lga in suburbsToLGA[suburb] if lga not in westernSydneyLGAs])
    context['non_ws_suburbs'] = str(getUniqueItems(nwss)).replace("'", '"')
    context['compare'] = compare
    context['info'] = getcompareinfo(compare, suburbsToLGA, lgaToRegion, westernSydneyLGAs)
    context['medianrent'] = getMedianRent(compare, findMatchingLGAs(compare, suburbsToLGA, lgaToRegion), westernSydneyLGAs)
    x = getAttractions()
    attractions = []
    for i in x:
        attractions.append({"url":x[i], "place":i})
    context['randomattractions'] = attractions

    x = getEvents()
    events = []
    for i in x:
        events.append({"url":x[i], "place":i})
    context['randomevents'] = events

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

import random

def getMedianRent(compare, LGAs, westernSydneyLGAs):
    medianRent, _ = getMedianWeeklyRent(LGAs)
    medianRentWest, lowest5WestLGA = getMedianWeeklyRent(westernSydneyLGAs)
    if medianRent is None or medianRentWest is None:
        return ''

    place = 'Western Sydney'
    # See if the rent for Western Sydney is lower. If not, find a low-rent area in Western Sydney to compare
    randomLowestRentLGAInTheWest = random.choice(list(lowest5WestLGA.keys()))
    if len(lowest5WestLGA) > 0 and medianRentWest >= medianRent and lowest5WestLGA[randomLowestRentLGAInTheWest] < medianRent:
        place = randomLowestRentLGAInTheWest
        medianRentWest = lowest5WestLGA[randomLowestRentLGAInTheWest]
    out = 'The median weekly rent for ' + place + ' is $' + str(medianRentWest) +\
          ', compared to $' + str(medianRent) + ' in ' + compare + '.'
    if medianRentWest < medianRent:
        out += ' That\'s an annual saving of $' + str((medianRent - medianRentWest) * 52) + '!'
    return out

def getAttractions():
    attractions = selectrandom2attractions()
    #out = 'You can also check out the great Western Sydney attractions: '
    #for place,url in attractions.iteritems():
    #    out += "<a href='" + url + "'>" + place + "</a>" + ","
    return attractions

def getEvents():
    events = selectrandom2events()
    #out = 'You can also check out the great Western Sydney attractions: '
    #for place,url in attractions.iteritems():
    #    out += "<a href='" + url + "'>" + place + "</a>" + ","
    return events
