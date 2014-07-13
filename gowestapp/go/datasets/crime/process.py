'''
Process raw data into dictionary: {state => {lga => {weekly rent bin => count}}}
e.g. {'New South Wales' => {'North Sydney' => {'$450-$549' => 2790}}}
'''
import csv
import os

class CrimeEntry:
    def __init__(self, total, ratePer100000, rank):
        self.total = total
        self.ratePer100000 = ratePer100000
        self.rank = rank

def process():
    file = open(os.path.dirname(os.path.realpath(__file__)) + '/data.csv', 'r')
    reader = csv.reader(file)
    results = {}
    lineCounter = 0
    for row in reader:
        if lineCounter != 2:
            lineCounter = lineCounter + 1
            continue
        #LGA
        # Stealing from person: Total,Rate per 100,000 population,Rank
        # Steal from motor vehicle: Total	Rate per 100,000 population	Rank
        # Robbery: Total	Rate per 100,000 population	Rank
        # Assault - Non-domestic violence: Total	Rate per 100,000 population	Rank
        # Assault - Domestic Violent: Total	Rate per 100,000 population	Rank
        # Sexual Offence: Total	Rate per 100,000 population	Rank
        lga = row[0]
        results[lga] = row[1:]
    return results

def getsomething():
    return "something"

def getCrimeRankStats():
    return process()

if __name__ == '__main__':
    print process()