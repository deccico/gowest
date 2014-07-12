'''
Process raw data into dictionary: {state => {lga => {weekly rent bin => count}}}
e.g. {'New South Wales' => {'North Sydney' => {'$450-$549' => 2790}}}
'''
import csv
def process():
    file = open('data.csv', 'r')
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

def getMedianWeeklyRent(LGAs):
    data = process()

    rentbins = {}   # dict of {rentbin: count}
    total = 0
    for lga in LGAs:
        for statev in data.values():
            if lga in statev:
                lgav = statev[lga]
                for rentbin, number in lgav.iteritems():
                    if rentbin not in rentbins:
                        rentbins[rentbin] = 0
                    rentbins[rentbin] += number
                    total += number
                break

    if total > 0:
        # Find median
        cumsum = 0
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