'''
Load CSV of region,LGA,suburb,postcode, and returns multiple dicts:
- Dict of suburb => [list of LGAs]
- Dict of LGA => region
'''
import csv
import os


def process():
    reader = csv.reader(open(os.path.dirname(os.path.realpath(__file__)) + '/data.csv', 'r'))
    isfirst = True
    suburbDict = {}
    lgaDict = {}
    for row in reader:
        if isfirst:
            isfirst = False
            continue
        #Sydney Outer,Auburn City Council,AUBURN NORTH,2144,

        region = row[0]

        # Remove extra strings in LGA names
        lga = row[1].replace(' City Council', '')\
            .replace('The Council of the Municipality of ', '')\
            .replace('Council of the City of ', '')\
            .replace(' Shire Council', '')\
            .replace(' Municipal Council', '')\
            .replace(' Council', '')\
            .replace(' Shire Counc', '')

        # Title capitalise
        suburb = ' '.join(w.capitalize() for w in row[2].split())

        # Ignore rubbish rows
        if 'nsw.gov.au' in suburb:
            continue

        if suburb not in suburbDict:
            suburbDict[suburb] = []
        if lga not in suburbDict[suburb]:
            suburbDict[suburb].append(lga)

        lgaDict[lga] = region

    return suburbDict, lgaDict

if __name__ == '__main__':
    print process()