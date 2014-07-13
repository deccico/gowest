from cPickle import load

f = open("out.pkl", "wb")
data = load(f)
f.close()

postCodes = data.keys()
postCodes.sort()

for postCode in postCodes:
    print data[postCode]
    raise NotImplementedError