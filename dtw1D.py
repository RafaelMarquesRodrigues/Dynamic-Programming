
import time
import queue
import multiprocessing
import threading
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
    for i in range(1, len(test) + 1):
        for j in range(1, len(training) + 1):
            values[i][j] = (test[i-1] - training[j-1]) * (test[i-1] - training[j-1]) + min(values[i-1][j-1], values[i][j-1], values[i-1][j])
    
    #return the dtw value accordingly to the size of the series
    return values[len(test)][len(training)]
        

#####################################################################################
#                       CALCULATING MOVEMENTS
#####################################################################################

def processFiles(title, test_filename, training_filename, label_filename):
    print("**************", title, "**************", sep='\n')

    #read files
    test_data = readFile(test_filename)
    training_data = readFile(training_filename)
    label = readLabel(label_filename)

    cores = multiprocessing.cpu_count()

    print("Calculating movements using {} threads...".format(cores))

    threads = [None] * cores
    q = queue.Queue(cores)
    counter = [0] * cores

    for i in range(0, cores):
        threads[i] = threading.Thread(group=None, target=startCalculation, args=(test_data, training_data, i * int(len(test_data)/cores), (i + 1) * int(len(test_data)/cores), q, counter, i))
	
    start = time.time()

    for i in range(0, cores):
        threads[i].start()
     
    thread_stop = threading.Event()
    threading.Thread(group=None, target=printProgress, args=(thread_stop, counter, cores, len(test_data))).start()

    for i in range(0, cores):
        threads[i].join()
    
    thread_stop.set()
    hits = 0

    while(not q.empty()):
        hits = hits + q.get()

    print("Accuracy:", hits/len(test_data))
    print("Time spent: ", time.time() - start)

def printProgress(thread_stop, counter, cores, total):

    while(not thread_stop.is_set()):
        time.sleep(0.5)
        calculated = 0
   
        for i in range(0, cores):
            calculated = calculated + counter[i]

        print("[{}/{}]\r".format(calculated, total), end='')


def startCalculation(test_data, training_data, lowerBound, upperBound, q, counter, index):
    hits = 0

    #for each test key calculate dtw and compare with the training key
    for test_series in test_data[lowerBound:upperBound]:
        result = sys.float_info.max
        
        #calculating dtw for each training series with the actual test series
        for training_series in training_data:
            aux = calculateDtw(test_series.getArray(), training_series.getArray())

            if(aux < result):
                result = aux
                selectedLabel = training_series.getLabel()
        
        #add a hit if correct
        if selectedLabel == test_series.getLabel():
            hits = hits + 1
        
        counter[index] = counter[index] + 1

    q.put(hits)

if __name__ == "__main__":
    processFiles("Rotulos 1D", "test.in", "training.in", "label.in")
