
test_filename = 'test.in'
training_filename = 'training.in'
label_filename = 'label.in'


def readFile(filename):
    d = {}
    
    with open(filename) as f:
        for line in f:
            content = line.split()
            d[int(content[0])] = [float(x) for x in content]

    return d

def getLabel(filename):
    d = {}
    
    with open(filename) as f:
        for line in f:
            content = line.split()
            d[int(content[0])] = content[1]

    return d
            
def printDict(d):
    keys = d.keys()

    for key in keys:
        print(key, d[key])

def dtw(test, training, i, j):
    if i < 0 or j < 0:
        return 0
    
    value = (float(test[i]) - float(training[j])) * (float(test[i]) - float(training[j]))
    
    print(i, j)

    return value + min(dtw(test, training, i-1, j-1), dtw(test, training, i, j-1), dtw(test, training, i-1, j))


test_data = readFile(test_filename)
training_data = readFile(training_filename)
label = getLabel(label_filename)

#printDict(test_data)
#printDict(training_data)
#printDict(label)

keysA = list(test_data.keys())
keysB = list(training_data.keys())

a = test_data[keysA[0]]
b = training_data[keysB[0]]

print(dtw(a, b, len(a)-1, len(b)-1))



