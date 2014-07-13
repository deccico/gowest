'''
Get dictionary of {suburb => [avg number of monthly fines, avg fine value]}
'''
import csv
import os


def getRedLightFinesBySuburb():
    file = open(os.path.dirname(os.path.realpath(__file__)) + '/data.csv', 'r')
    isfirst = True
    reader = csv.reader(file)
    # Start by storing totals so we can calculate weighted average later
    resultTotals = {}   # dict of suburb => [list of [number, totalvalue]]
    for row in reader:
        if isfirst:
            isfirst = False
            continue
        #2007/08,Apr,1,318,Red Light Camera,Not Stop At Red Light - Camera Detected - Corporation,STONEY CREEK ROAD (140) PEAKHURST WESTBOUND
        number = int(row[2])
        totalvalue = int(row[3])
        address = row[6]    #STONEY CREEK ROAD (140) PEAKHURST WESTBOUND
        # Split the address - grab the suburb (after the parens, before the last word)
        suburb = address[address.find(')')+2:]
        # Strip 'bound' from result
        if 'BOUND' in suburb and ' ' in suburb:
            suburb = suburb[:suburb.rfind(' ')]
        # Some suburbs names have parens
        if '(Z)' in suburb:
            suburb = suburb[:suburb.find('(')]
        if ')' in suburb:
            suburb = suburb[suburb.rfind(')')+1:]
        if 'O/RAMP' in suburb:
            suburb = suburb[suburb.find('O/RAMP')+7:]
        suburb = ' '.join(w.capitalize() for w in suburb.split())   # title capitalise

        if suburb not in resultTotals:
            resultTotals[suburb] = []
        resultTotals[suburb].append([number, totalvalue])
    # now calculate averages
    results = {}
    for suburb, totals in resultTotals.iteritems():
        months = 0
        totalfines = 0
        totalfinevalue = 0
        for total in totals:
            months += 1
            totalfines += total[0]
            totalfinevalue += total[1]
        numbermonthly = totalfines / months
        avgvalue = totalfinevalue / totalfines
        results[suburb] = [numbermonthly, avgvalue]
    return results


if __name__ == '__main__':
    print getRedLightFinesBySuburb()