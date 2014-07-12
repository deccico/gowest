'''
Process raw data into dictionary: {state => {lga => {weekly rent bin => count}}}
e.g. {'New South Wales' => {'North Sydney' => {'$450-$549' => 2790}}}
'''
import csv
import os
import random
def process():
    file = open(os.path.dirname(os.path.realpath(__file__)) + '/data.csv', 'r')
    reader = csv.reader(file)
    results = {}
    for row in reader:
        description_URL = row[0]
        activity_name = row[1]
        addrow(results, activity_name, description_URL)
    return results

def getsomething():
    return "something"

def addrow(results, activity_name, description_URL):
    results[activity_name] = description_URL

def selectrandom2attractions():
    attractions =  random.sample(process(), 2)
    resultDict = {}
    resultDict[attractions[0]] = process()[attractions[0]]
    resultDict[attractions[1]] = process()[attractions[1]]
    return resultDict

if __name__ == '__main__':
    print process()