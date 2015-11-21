
import operator
import sys

class Series:
    
    def __init__(self, l, a):
        self.label = l
        self.array = a

    def getLabel(self):
        return self.label

    def getArray(self):
        return self.array

def readFile(filename):
    d = []
    
    with open(filename) as f:
        for line in f:
            float_array = []
            content = line.split()
            
            #reads the series
            float_array = [float(x) for x in content[1:]]

            d.append(Series(int(content[0]), float_array))  

    return d

#reads all the labels
def readLabel(filename):
    d = {}

    with open(filename) as f:
        for line in f:
            content = line.split()
            d[int(content[0])] = content[1]

    return d;

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
    test_data = readFile(test_filename)
    training_data = readFile(training_filename)
    label = readLabel(label_filename)

    hits = 0
    counter = 0

    #for each test key calculate dtw and compare with the training key
    for test_series in test_data:
        result = sys.float_info.max
        
        #calculating dtw for each training series with the actual test series
        for training_series in training_data:
            aux = calculateDtw(test_series.getArray(), training_series.getArray())

            if(aux < result):
                result = aux
                selectedLabel = training_series.getLabel()
        
        #get the best result from them
        #print("DTW:", "{0:.12f}".format(result), "Class:", label[selectedLabel], end=(' '*(20 - len(label[selectedLabel]))))
        
        #add a hit if correct
        if selectedLabel == test_series.getLabel():
            hits = hits + 1
        #    print("Hit.")
        #else:
        #    print("Miss ({}) .".format(label[test_series.getLabel()]))

        counter = counter + 1
        print("[{}/{}]\r".format(counter, len(test_data)), end='')

    print("Accuracy:", hits/len(test_data))

processFiles("Rotulos 1D", "test.in", "training.in", "label.in")

#precisa fazer a extensão pra calcular esse
#processFiles("Rotulos 3D", "test3D.in", "training3D.in", "label3D.in")

