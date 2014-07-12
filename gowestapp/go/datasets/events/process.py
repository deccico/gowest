'''
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
        event_name = row[1]
        addrow(results, event_name, description_URL)
    return results

def getsomething():
    return "something"

def addrow(results, event_name, description_URL):
    results[event_name] = description_URL

def selectrandom2events():
    events =  random.sample(process(), 2)
    resultDict = {}
    resultDict[events[0]] = process()[events[0]]
    resultDict[events[1]] = process()[events[1]]
    return resultDict

if __name__ == '__main__':
    print process()