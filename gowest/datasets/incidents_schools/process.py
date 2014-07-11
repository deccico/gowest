'''
Process raw data into dictionary: {region => {type => {year => {term => number}}}}
e.g. {'Hunter/Central Coast' => {'Assault' => {2012 => {1 => 20}}}}
'''
def process_2012(file, term):
    year = 2012
    isfirst = True
    results = {}
    types = []
    for line in file:
        if isfirst:
            #REGION Assault Threats Weapons Drugs Other TOTAL
            cols = line.split()
            # Add incident types
            for i in range(1, len(cols) - 2):
                types.append(cols[i])
            isfirst = False
        else:
            #Hunter/Central Coast 20 8 4 1 2 35
            cols = line.split()
            # Collect non-numeric elements as region name
            regiontokens = []
            for col in cols:
                if col.isdigit():
                    break
                regiontokens.append(col)
            region = ' '.join(regiontokens)
            typeindex = 0
            for col in cols:
                if not col.isdigit():
                    continue
                type = types[typeindex]
                number = int(col)
                if region not in results:
                    results[region] = {}
                if type not in results[region]:
                    results[region][type] = {}
                if year not in results[region][type]:
                    results[region][type][year] = {}
                results[region][type][year] = {term: number}
                typeindex += 1
                if typeindex == len(types):
                    break
    return results

from os import walk
def process():
    f = []
    for (dirpath, dirnames, filenames) in walk('.'):
        f.extend(filenames)
        break
    allresults = {}
    for filename in f:
        if filename.startswith('2012'):
            #2012_1.txt
            term = filename[filename.find('_')+1:filename.find('.')]
            results = process_2012(open(filename, 'r'), term)
            for region, regionv in results.items():
                if region not in allresults:
                    allresults[region] = {}
                for type, typev in regionv.items():
                    if type not in allresults[region]:
                        allresults[region][type] = {}
                    for year, yearv in typev.items():
                        allresults[region][type][year] = yearv
    return allresults

if __name__ == '__main__':
    print process()