
import operator
import sys

#creates a dictionary with 'class': [numbers of the series] or 'class': name of the class, if its used to read the label
def readFile(filename, function):
    d = {}
    
    with open(filename) as f:
        for line in f:
            content = line.split()
            d[int(content[0])] = function(content)

    return d

def getFloatContent(content):
    return [float(x) for x in content]

def getStrContent(content):
    return content[1]

def calculateDtw(test, training):
    #start the matrix with max float values
    values = [[sys.float_info.max for i in range(0, len(training) + 1)] for j in range(0, len(test) + 1)]
   
    #(0, 0) position starts with 0
    values[0][0] = 0.0
    
    #calculate the value for each position on the matrix
    for i in range(1, len(test)):
        for j in range(1, len(training)):
            values[i][j] = (test[i] - training[j]) * (test[i] - training[j]) + min(values[i-1][j-1], values[i][j-1], values[i-1][j])
    
    #return the dtw value accordingly to the size of the series
    return values[len(test)-1][len(training)-1]
        

#####################################################################################
#                       CALCULATING MOVEMENTS
#####################################################################################

def processFiles(title, test_filename, training_filename, label_filename):
    print("**************", title, "**************", sep='\n')

    #read files
    test_data = readFile(test_filename, getFloatContent)
    training_data = readFile(training_filename, getFloatContent)
    label = readFile(label_filename, getStrContent)

    #get list of keys
    test_keys = test_data.keys()
    training_keys = training_data.keys()

    hits = 0

    #for each test key calculate dtw and compare with the training key
    for test_key in test_keys:
        d = {}
        
        #calculating dtw for each training series with the actual test series
        for training_key in training_keys:
            d[training_key] = calculateDtw(test_data[test_key], training_data[training_key])
        
        #sort all the dtw calculated
        results = sorted(d.items(), key=operator.itemgetter(1))
        
        #get the best result from them
        print("DTW:", results[0][1], "Class:", label[results[0][0]], end=(' '*(20 - len(label[results[0][0]]))))
        
        #add a hit if correct
        if results[0][0] == test_key:
            hits = hits + 1
            print("\tHit.")
        else:
            print("\tMiss ({}) .".format(label[test_key]))

    print("Accuracy:", hits/len(test_keys))

processFiles("Rotulos 1D", "test.in", "training.in", "label.in")

#precisa fazer a extensão pra calcular esse
#processFiles("Rotulos 3D", "test3D.in", "training3D.in", "label3D.in")

