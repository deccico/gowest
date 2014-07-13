'''
Process raw data into dictionary: {state => {lga => {weekly rent bin => count}}}
e.g. {'New South Wales' => {'North Sydney' => {'$450-$549' => 2790}}}
'''

import os
from random import choice

def loadData():
    f = open(os.path.dirname(os.path.realpath(__file__)) + '/data.csv', 'r')
    x = f.read()
    f.close()
    x = x.split("\n")
    keys = [i.strip() for i in x[0].split(",")]
    x = x[1:]
    data = {}
    for i in x:
        try:
            line = i.split(",")
            line = [j.strip() for j in line]
            postCode = line[0]
            lineData = {}
            for j in xrange(1, len(line)):
                lineData[keys[j]] = line[j]
            data[postCode] = lineData
        except:
            pass
    return data


def getCostOfLiving(suburb, postCode, westernSydneyPostcodes, suburbToPostcode):
    data = loadData()

    rent = int(data[postCode]["Median weekly rent"])
    mortgage = int(data[postCode]["Median monthly mortgage"])

    postcodeToSuburb = {}
    for i in suburbToPostcode:
        postcodeToSuburb[suburbToPostcode[i]] = i

    westRent = [[int(data[i]["Median weekly rent"]), postcodeToSuburb[i]] for i in westernSydneyPostcodes if data.has_key(i)]
    westMort = [[int(data[i]["Median monthly mortgage"]), postcodeToSuburb[i]] for i in westernSydneyPostcodes if data.has_key(i)]
    westRent.sort()
    westMort.sort()

    betterRent = []
    betterMort = []
    for i in westRent:
        if i[0] < rent:
            betterRent.append(i)

    for i in westMort:
        if i[0] < mortgage:
            betterMort.append(i)

    textLines = []

    try:
        betterRent = betterRent[10:len(betterRent) / 2 + 1]
        rentComp = choice(betterRent)
        textLines.append("Did you know that the average rent in %s is $%d per week, for a saving of $%d per year over %s?" % (rentComp[1], rentComp[0], (rent - rentComp[0]) * 52, suburb))
    except:
        pass

    try:
        betterMort = betterMort[10:len(betterMort) / 2 + 1]
        mortComp = choice(betterMort)
        textLines.append("If you lived in %s as opposed to %s, you could save %d%% on your mortgage - that's $%d per year!" % (mortComp[1], suburb, int(((mortgage - mortComp[0]) / float(mortgage))*100), (mortgage - mortComp[0]) * 12))
    except:
        pass

    if(len(textLines) == 0):
        textLines = ["%s is just as affordable as Western Sydney!" % (suburb, )]

    return {"heading" : "Cost of Living", "text" : textLines}