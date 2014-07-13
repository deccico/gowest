from django.shortcuts import render

from go.datasets.lga_suburb_list import process
from go.datasets.attractions.process import selectrandom2attractions
from go.datasets.events.process import selectrandom2events
from go.datasets.red_light_camera_notices.process import getRedLightFinesBySuburb
from go.datasets.crime.process import getCrimeRankStats
from go.datasets.census_preproc.process import getCostOfLiving
from go.datasets.travel_method.process import getPercentCommutersByType
import random

def index(request):
    westernSydneyLGAs = ['Auburn', 'Bankstown', 'Blacktown', 'Blue Mountains', 'Camden', 'Campbelltown', 'Fairfield', 'Hawkesbury', 'The Hills', 'Holroyd', 'Liverpool', 'Parramatta', 'Penrith', 'Wollondilly']
    context = {}
    suburbsToLGA, lgaToRegion, suburbToPostcode = process.process()
    compare = ' '.join(w.capitalize() for w in request.GET.get('compare', '').strip().split())    # trim and title capitalise
    nwss = sorted([suburb for suburb in suburbsToLGA.keys() for lga in suburbsToLGA[suburb] if lga not in westernSydneyLGAs])
    westernSydneySuburbs = [suburb for suburb in suburbsToLGA.keys() for lga in suburbsToLGA[suburb] if lga in westernSydneyLGAs]
    compareSuburbs = findMatchingSuburbs(compare, suburbsToLGA, lgaToRegion)
    isWesternSydney = False
    for i in compareSuburbs:
        if i in westernSydneySuburbs:
            isWesternSydney = True

    allsuburbs = sorted(list(set(suburbsToLGA.keys())))

    context['non_ws_suburbs'] = str(getUniqueItems(nwss)).replace("'", '"')
    context['autocomplete'] = str(getUniqueItems(allsuburbs)).replace("'", '"')
    context['compare'] = compare
    context['isWesternSydney'] = isWesternSydney
    context['info'] = getcompareinfo(compare, suburbsToLGA, lgaToRegion, westernSydneyLGAs)
    matchedLGAs = findMatchingLGAs(compare, suburbsToLGA, lgaToRegion)

    westernSydneyPostcodes = list(set([suburbToPostcode[i] for i in westernSydneySuburbs if i in suburbToPostcode]))

    try:
        postCode = suburbToPostcode[findMatchingSuburbs(compare, suburbsToLGA, lgaToRegion)[0]]
        context['costOfLiving'] = getCostOfLiving(compare, postCode, westernSydneyPostcodes, suburbToPostcode)
    except:
        pass

    context['crimerank'] = getCrimeRank(matchedLGAs, westernSydneyLGAs)

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
    context['redlightfines'] = getRedLightFines(compare, findMatchingSuburbs(compare, suburbsToLGA, lgaToRegion), westernSydneySuburbs)
    context['gogreen'] = getGreenTransport(compare, matchedLGAs, westernSydneyLGAs)
    return render(request, 'go/index.html', context)

def getUniqueItems(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

# Get an LGA given the input; if the input is a suburb find its LGA
def findMatchingLGAs(compare, suburbToLGA, lgaToRegion):
    if compare in lgaToRegion:
        return [compare]
    elif compare in suburbToLGA:
        return suburbToLGA[compare]
    return []

# Get a list of suburbs given the input; if the input is an LGA find all its suburbs
def findMatchingSuburbs(compare, suburbToLGA, lgaToRegion):
    if compare in suburbToLGA:
        return [compare]
    elif compare in lgaToRegion:
        return getSuburbsInLGA(compare, suburbToLGA)
    return []

def getSuburbsInLGA(lga, suburbToLGA):
    return [s for s in suburbToLGA.keys() for l in suburbToLGA[s] if l == lga]

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
        return None

    place = 'Western Sydney'
    # See if the rent for Western Sydney is lower. If not, find a low-rent area in Western Sydney to compare
    randomLowestRentLGAInTheWest = random.choice(list(lowest5WestLGA.keys()))
    if len(lowest5WestLGA) > 0 and medianRentWest >= medianRent and lowest5WestLGA[randomLowestRentLGAInTheWest] < medianRent:
        place = randomLowestRentLGAInTheWest
        medianRentWest = lowest5WestLGA[randomLowestRentLGAInTheWest]
    if medianRentWest >= medianRent:
        return None

    out = {}
    out['heading'] = 'Affordable living'
    out['text'] = ['The median weekly rent for ' + place + ' is $' + str(medianRentWest) +
                   ', compared to $' + str(medianRent) + ' in ' + compare + '.',
                   'That\'s an annual saving of $' + str((medianRent - medianRentWest) * 52) + '!']
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

def getCrimeRank(matchedLGAs, westernSydneyLGAs):
    random.shuffle(westernSydneyLGAs)
    outputStr = "Did you know that {0} has a significantly worse issue with {2} (Ranked {1}th) than {3} (Ranked {4}th)?"
    dataset = getCrimeRankStats()
    for matchedLGA in matchedLGAs:
        if matchedLGA in dataset:
            matchedLGARank = dataset[matchedLGA]
            for westernSydneyLGA in westernSydneyLGAs:
                if westernSydneyLGA in dataset:
                    westernSydneyLGARank = dataset[westernSydneyLGA]
                    #compare the rank
                    if matchedLGARank[2].strip() != '-' and matchedLGARank[2].strip() != 'nc' and \
                        westernSydneyLGARank[2].strip() != '-' and westernSydneyLGARank[2].strip() != 'nc' and \
                        float(matchedLGARank[2]) < float(westernSydneyLGARank[2]):
                        #return matchedLGA+":"+str(matchedLGARank[2])+" vs "+westernSydneyLGA + ":" + str(westernSydneyLGARank[2])
                        # + " " + str(matchedLGARank) + " " + str(westernSydneyLGARank)
                        return outputStr.format(matchedLGA,matchedLGARank[2],"personal theft", westernSydneyLGA, westernSydneyLGARank[2])
                    elif matchedLGARank[5].strip() != '-' and matchedLGARank[5].strip() != 'nc' and \
                        westernSydneyLGARank[5].strip() != '-' and westernSydneyLGARank[5].strip() != 'nc' and \
                        float(matchedLGARank[5]) < float(westernSydneyLGARank[5]):
                        return outputStr.format(matchedLGA,matchedLGARank[5],"theft from a motor vehicle", westernSydneyLGA, westernSydneyLGARank[5])
                    elif matchedLGARank[8].strip() != '-' and matchedLGARank[8].strip() != 'nc' and \
                        westernSydneyLGARank[8].strip() != '-' and westernSydneyLGARank[8].strip() != 'nc' and \
                        float(matchedLGARank[8]) < float(westernSydneyLGARank[8]):
                        return outputStr.format(matchedLGA,matchedLGARank[8],"robbery", westernSydneyLGA, westernSydneyLGARank[8])
                    elif matchedLGARank[11].strip() != '-' and matchedLGARank[11].strip() != 'nc' and \
                        westernSydneyLGARank[11].strip() != '-' and westernSydneyLGARank[11].strip() != 'nc' and \
                        float(matchedLGARank[11]) < float(westernSydneyLGARank[11]):
                        return outputStr.format(matchedLGA,matchedLGARank[11],"non-domestic assault", westernSydneyLGA, westernSydneyLGARank[11])
                    elif matchedLGARank[14].strip() != '-' and matchedLGARank[14].strip() != 'nc' and \
                        westernSydneyLGARank[14].strip() != '-' and westernSydneyLGARank[14].strip() != 'nc' and \
                        float(matchedLGARank[14]) < float(westernSydneyLGARank[14]):
                        return outputStr.format(matchedLGA,matchedLGARank[14],"domestic assault", westernSydneyLGA, westernSydneyLGARank[14])
                    elif matchedLGARank[17].strip() != '-' and matchedLGARank[17].strip() != 'nc' and \
                        westernSydneyLGARank[17].strip() != '-' and westernSydneyLGARank[17].strip() != 'nc' and \
                        float(matchedLGARank[17]) < float(westernSydneyLGARank[17]):
                        return outputStr.format(matchedLGA,matchedLGARank[17],"sexual offences", westernSydneyLGA, westernSydneyLGARank[17])

    return "Congrats, your area is just as safe as Western Sydney in 2013."

def getRedLightFines(compare, suburbs, westernSydneySuburbs):
    if len(suburbs) == 0:
        return None
    fines = getRedLightFinesBySuburb()
    avgnumber, avgfine = getRedLightFinesForSuburbs(suburbs, fines)
    avgnumberwest, avgfinewest = getRedLightFinesForSuburbs(westernSydneySuburbs, fines)
    if avgnumber is None:
        return None

    out = {}
    if avgnumber > avgnumberwest:
        out['heading'] = 'Safer driving'
        out['text'] = ['The average annual count of red light offences for Western Sydney is ' + str(avgnumberwest) +
                       ', as opposed to to ' + str(avgnumber) + ' in ' + compare + '.']
        return out
    elif avgfine > avgfinewest:
        out['heading'] = 'Affordable'
        out['text'] = ['The average red light fine for Western Sydney is $' + str(avgfinewest) +
                       ', as opposed to $' + str(avgfine) + ' in ' + compare + '.',
                       'You save $' + str(avgfine - avgfinewest) + '!']
        return out
    return None

def getRedLightFinesForSuburbs(suburbs, fines):
    totalnumber = 0
    totalfines = 0
    suburbsfound = 0
    for suburb in suburbs:
        if suburb in fines:
            totalnumber += fines[suburb][0]
            totalfines += fines[suburb][1]
            suburbsfound += 1
    if suburbsfound > 0:
        return totalnumber / suburbsfound, totalfines / suburbsfound
    return None, None

def getGreenTransport(compare, LGAs, westernSydneyLGAs):
    pctbike = getPercentCommutersByType(LGAs, 'bikeorwalk')
    pctpublic = getPercentCommutersByType(LGAs, 'publictransport')
    pctbikewest = getPercentCommutersByType(westernSydneyLGAs, 'bikeorwalk')
    pctpublicwest = getPercentCommutersByType(westernSydneyLGAs, 'publictransport')
    winratiobike = 0
    if pctbikewest > 0:
        winratiobike = (pctbikewest - pctbike) / pctbikewest
    winratiopublic = 0
    if pctpublicwest > 0:
        winratiopublic = (pctpublicwest - pctpublic) / pctpublicwest
    if winratiobike <= 0 and winratiopublic <= 0:
        return None
    out = {}
    out['heading'] = 'Sustainable living'
    if winratiobike > winratiopublic:
        out['text'] = [('%.1f' % (pctbikewest * 100)) + '% of Western Sydneysiders bicycled or walked to work.',
                       'That\'s more than the ' + ('%.1f' % (pctbike * 100)) + '% in ' + compare + '!']
    else:
        out['text'] = [('%.1f' % (pctpublicwest * 100)) + '% of Western Sydneysiders took public transport to work.',
                       'That\'s more than the ' + ('%.1f' % (pctpublic * 100)) + '% in ' + compare + '!']
    return out
