'''
Process raw data into dictionary: {state => {suburb => {weekly rent bin => count}}}
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
        suburb = row[2][:row[2].rfind(' ')]    # ignore last token (C)
        rentbin = row[5]
        number = int(row[7])
        addrow(results, state, suburb, rentbin, number)
    return results

def addrow(results, state, suburb, rentbin, number):
    if state not in results:
        results[state] = {}
    if suburb not in results[state]:
        results[state][suburb] = {}
    if rentbin not in results[state][suburb]:
        results[state][suburb][rentbin] = 0
    results[state][suburb][rentbin] += number

if __name__ == '__main__':
    print process()