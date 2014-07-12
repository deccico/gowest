'''
Process raw data into dictionary: {state => {lga => {weekly rent bin => count}}}
e.g. {'New South Wales' => {'North Sydney' => {'$450-$549' => 2790}}}
'''
import csv
def process():
    file = open('data.csv', 'r')
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

if __name__ == '__main__':
    print process()