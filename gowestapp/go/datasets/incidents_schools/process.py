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
                addresult(results, region, type, year, term, number)
                typeindex += 1
                if typeindex == len(types):
                    break
    return results

def process_old(file):
    text = ' '.join(file.readlines())
    # Tokenise whole thing
    tokens = text.split()
    state = 'start'
    year = None
    terms = []
    termindex = 0
    categories = ['Assault', 'Drugs', 'Other', 'Threats', 'Weapons']
    regiontokens = []
    results = {}
    data = []
    for token in tokens:
        if state == 'start':
            if 'Term' == token:
                #Term 1, 2011 Term 2, 2011
                state = 'termyears'
        elif state == 'termyears':
            if ',' in token:
                #Term 1, 2011 Term 2, 2011
                term = token[:-1]
                terms.append(term)
            elif token.isdigit():
                year = token
            elif token == 'Region':
                state = 'data'
                regiontokens = []
        elif state == 'data':
            if token in categories or token == 'Total' or token == 'Region':
                continue
            if not token.isdigit():
                #Hunter/Central
                #Coast
                if len(data) > 0:
                    region = ' '.join(regiontokens)
                    term = terms[termindex]
                    for category, number in zip(categories, data):
                        addresult(results, region, category, year, term, number)
                    termindex = 1 - termindex
                    data = []
                    regiontokens = []
                if token == 'Term':
                    state = 'termyears'
                    terms = []
                    termindex = 0
                    regiontokens = []
                    continue
                regiontokens.append(token)
            else:
                #13
                #4
                data.append(token)
    if len(data) > 0:
        region = ' '.join(regiontokens)
        term = terms[termindex]
        for category, number in zip(categories, data):
            addresult(results, region, category, year, term, number)
    return results

def addresult(results, region, type, year, term, number):
    if region not in results:
        results[region] = {}
    if type not in results[region]:
        results[region][type] = {}
    if year not in results[region][type]:
        results[region][type][year] = {}
    results[region][type][year] = {term: number}

from os import walk
def process():
    f = []
    for (dirpath, dirnames, filenames) in walk('.'):
        f.extend(filenames)
        break
    allresults = {}
    for filename in f:
        results = {}
        if filename.startswith('2012'):
            #2012_1.txt
            term = filename[filename.find('_')+1:filename.find('.')]
            results = process_2012(open(filename, 'r'), term)
        elif filename == '2005-2011.txt':
            results = process_old(open(filename, 'r'))
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