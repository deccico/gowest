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
        number = int(row[7])
        addrow(results, state, lga, rentbin, number)
    return results

def getsomething():
    return "something"

def addrow(results, state, lga, rentbin, number):
    if state not in results:
        results[state] = {}
    if lga not in results[state]:
        results[state][lga] = {}
    if rentbin not in results[state][lga]:
        results[state][lga][rentbin] = 0
    results[state][lga][rentbin] += number

if __name__ == '__main__':
    print process()