'''
Process CSV containing number of people travelling to work by method, and output dictionary
{suburb => {travel method => number}}
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
        #"Local Government Areas (2011)","South Australia","Tea Tree Gully (C)","Annual","2011","Train","Persons",33,
        lga = row[2][:row[2].rfind(' ')]    # ignore last token (C)

        # Special LGA name replacements
        if lga == 'The Hills Shire':
            lga = 'The Hills'

        '''
        "Bicycle"
        "Bus and 1 Other"
        "Bus and two other methods (excludes train)"
        "Bus"
        "Car
        "Did not go to work"
        "Ferry "
        "Method of travel to work not stated"
        "Motorbike/scooter"
        "Other three methods"
        "Other two methods"
        "Other"
        "Taxi"
        "Three methods:"
        "Total one method"
        "Total two methods"
        "Total"
        "Train and 1 Other:"
        "Train and two other methods"
        "Train"
        "Tram (includes light rail)"
        "Truck"
        "Walked only"
        "Worked at home"
        '''
        method = row[5].strip().split(' ')[0]
        # sanitise method
        if 'Total' in method or 'Three' in method:
            continue

        sex = row[6]
        if sex != 'Persons':
            continue

        number = int(row[7])

        addrow(results, lga, method, number)
    return results

def addrow(results, lga, method, number):
    if lga not in results:
        results[lga] = {}
    if method not in results[lga]:
        results[lga][method] = 0
    results[lga][method] += number


# type: 'publictransport', 'bikeorwalk'
def getPercentCommutersByType(LGAs, type):
    if type not in ('publictransport', 'bikeorwalk'):
        raise 'Invalid type'
    total = 0
    matched = 0
    data = process()
    for lga in LGAs:
        if lga in data:
            for method, number in data[lga].iteritems():
                if type == 'publictransport' and method in ('Bus', 'Ferry', 'Train', 'Tram'):
                    matched += number
                elif type == 'bikeorwalk' and method in ('Bicycle', 'Walked'):
                    matched += number
                total += number
    if total == 0:
        return 0
    return float(matched) / total

if __name__ == '__main__':
    print process()
    print getPercentCommutersByType(['Parramatta'], 'bikeorwalk')