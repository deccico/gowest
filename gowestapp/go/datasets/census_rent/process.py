'''
Process raw data into dictionary: {state => {lga => {weekly rent bin => count}}}
e.g. {'New South Wales' => {'North Sydney' => {'$450-$549' => 2790}}}
'''
import csv
import os


def process():
    file = open(os.path.dirname(os.path.realpath(__file__)) + '/data.csv', 'r')
    isfirst = True
    reader = csv.reader(file)
    results = {}
    for row in reader:
        if isfirst:
            isfirst = False
            continue
        #"Local Government Areas (2011)","New South Wales","Albury (C)","Annual","2011","$0-$74","Real estate agent",11,
        state = row[1]
        lga = row[2][:row[2].rfind(' ')]    # ignore last token (C)

        # Special LGA name replacements
        if lga == 'The Hills Shire':
            lga = 'The Hills'

        rentbin = row[5]
        if rentbin == 'Total':
            continue
        number = int(row[7])
        addrow(results, state, lga, rentbin, number)
    return results

def addrow(results, state, lga, rentbin, number):
    if state not in results:
        results[state] = {}
    if lga not in results[state]:
        results[state][lga] = {}
    if rentbin not in results[state][lga]:
        results[state][lga][rentbin] = 0
    results[state][lga][rentbin] += number


import operator

# Returns overall median, and lowest-5 LGA medians
def getMedianWeeklyRent(LGAs):
    data = process()

    rentbins = {}   # dict of {rentbin: count}
    rentbinsPerLGA = {}
    total = 0
    totalPerLGA = {}
    for lga in LGAs:
        for statev in data.values():
            if lga in statev:
                lgav = statev[lga]
                for rentbin, number in lgav.iteritems():
                    if lga not in rentbinsPerLGA:
                        rentbinsPerLGA[lga] = {}
                        totalPerLGA[lga] = 0

                    if rentbin not in rentbins:
                        rentbins[rentbin] = 0
                        rentbinsPerLGA[lga][rentbin] = 0
                    rentbins[rentbin] += number
                    rentbinsPerLGA[lga][rentbin] = number
                    total += number
                    totalPerLGA[lga] += number
                break

    if total > 0:
        # Find median
        cumsum = 0
        median = getMedianRent(rentbins, total)
        lowest5LGAMedians = {}
        if len(LGAs) == 1:
            lowest5LGAMedians = {LGAs[0], median}
        else:
            medianPerLGA = {}
            for lga in LGAs:
                medianPerLGA[lga] = getMedianRent(rentbinsPerLGA[lga], totalPerLGA[lga])
            lowest5LGAMedians = dict(sorted(medianPerLGA.iteritems(), key=operator.itemgetter(1))[:5])
        return median, lowest5LGAMedians
    return None

def getMedianRent(rentbins, total):
    cumsum = 0
    median = None
    for rentbin, count in iter(sorted(rentbins.iteritems())):
        cumsum += count
        if cumsum > total / 2:
            if '-' in rentbin:
                #$150-$199
                rentpair = rentbin.split('-')
                # Strip dollar sign
                rentlow = int(rentpair[0][1:])
                renthigh = int(rentpair[1][1:])
                return (rentlow + renthigh) / 2
            elif 'and over' in rentbin:
                #$650 and over
                return int(rentbin[1:rentbin.find(' and over')])
    return None

if __name__ == '__main__':
    print process()
    print getMedianWeeklyRent(['Sutherland Shire'])