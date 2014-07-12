'''
'''
import csv
def process():
    file = open('data.csv', 'r')
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

if __name__ == '__main__':
    print process()