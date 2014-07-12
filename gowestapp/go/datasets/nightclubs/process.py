'''
process each line of night clubs into a python dictionary entry
'''
import csv
def process():
    file = open('data.csv', 'r')
    reader = csv.reader(file)
    results = {}
    for row in reader:
        #Panthers World Of Entertainement (14 Bars), Cnr Mulgoa and Jamison Rds, Penrith, NSW, http://www.barsandnightclubs.com.au/sydney/sydney-west/panthers-world-of-entertainement-14-bars-/
        clubname = row[0]
        physical_address = ','.join(row[1:-1])
        cluburl = row[-1]
        addrow(results, clubname, physical_address, cluburl)
    return results

def getsomething():
    return "something"

def addrow(results, clubname, physical_address, cluburl):
    results[clubname] = [physical_address, cluburl]

if __name__ == '__main__':
    print process()