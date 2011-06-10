from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from dateutil import parser
import numpy as N
import pylab
import time

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from django.http import HttpResponse

# --------------------------- Helper Functions ------------------------------- #

# read_array reads in values from a csv and output an 2D array with
# the csv's info 
# Input:  filename - name of the file to read from
#         dtype - list of pairs (field name, variable type) *what is this for?
#         separator - char that comes between terms, default is comma
# Output: 2D array - (2D array)[i] is column i of the csv file 
def read_array(filename, dtype, separator=','):
    data = [[] for dummy in xrange(len(dtype))]
    f = open(filename, 'r')
    for line in f:
        fields = line.strip().split(separator)
        index = len(fields)
        if index > len(data):
            index = len(data)
        for i in range(index):
            number = fields[i]
            data[i].append(number)
    f.close()
    return data

# det_majority takes in a range of points and determines their majority 'mode'
# value. In the event of a tie, returns the smallest index of a majority
# Input:  array - array to read from
#         modes - array of values to compare array elements to; currently only 4
#         values allowed *make this generalized?!
# Output: index of the majority value in the modes array
def det_majority(array, modes):
    frequency= [0, 0, 0, 0]
    for i in range(len(array)):
        temp = str(array[i])
        if temp == modes[0]:
            frequency[0] = frequency[0] + 1
        elif temp == modes[1]:
            frequency[1] = frequency[1] + 1
        elif temp == modes[2]:
            frequency[2] = frequency[2] + 1
        elif temp == modes[3]:
            frequency[3] = frequency[3] + 1
        else:
            print temp
            return -1
    majority = 0
    for i in range(len(frequency)):
        if frequency[i] > frequency[majority]:
            majority = i
    return majority

# det_mean takes in an array of date/times and outputs the mean of the times
# Input:  array - array to read from
# Output: mean of the values in the array
def det_mean(array):
    mn = parser.parse(array[0])
    mx = parser.parse(array[len(array) - 1])
    avg = mn + ((mx - mn) / (len(array) - 1))
    return avg.strftime("%H:%M")

# -------------------------------- Main Function ----------------------------- #
#clf()  ## clear the window

#plot(x, y2, 'r', label="Gallup", color='r', linewidth=2, markerfacecolor='g',
#    markeredgecolor='y', marker='d')

# Add Legend
#legend()
def plot_chart(filename):

    # Read in the csv and translate the modes into ints
    y_axis_labels =  ['still', 'drive', 'walk', 'bike']
    x_axis_labels = []
    x = []      #x values
    y = []      #y values
    descr = N.dtype([('#id', 'string'), ('user_id', 'string'),
                     ('time_stamp', 'string'), ('epoch_millis', 'string'),
                     ('phone_timezone', 'string'), ('latitude', 'string'),
                     ('longitude', 'string'), ('mode', 'string'),
                     ('speed', 'string')])
    myrecarray = read_array(filename, descr)
    
    # Reduce the number of visible points by aggregating
    # variables for aggregation to ~120 points
    array_len = len(myrecarray[7])
    grouping = array_len / 120
    if grouping > 0:
        points_limit = array_len / grouping
    else:
        points_limit = array_len
    
    # Aggregate and add the points to our x and y values
    i = 1                                      ### determine format of csv!!!
    while i < array_len:
        if i + grouping > array_len:
            temp = det_majority((myrecarray[7])[i:array_len], y_axis_labels)
            mean_time = det_mean((myrecarray[2])[i:array_len])
        else:
            temp = det_majority((myrecarray[7])[i:i+grouping], y_axis_labels)
            mean_time = det_mean((myrecarray[2])[i:i+grouping])
        x.append(i)
        x_axis_labels.append(mean_time)
        if temp == 0:
            y.append(.5)
        elif temp == 1:
            y.append(1.5)
        elif temp == 2:
            y.append(2.5)
        elif temp == 3:
            y.append(3.5)
        else:
            x.remove(i)
            x_axis_labels.remove(mean_time)
        i = i + grouping
    
    print len(y)
    # ------------------------- Define How Graph Looks ----------------------- #
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.grid(True)   # put grid lines on the graph for readibility
    
    # Graph and axis titles
    xlabel('Time of Day')
    ylabel('Mode')
    title('Activity for ' + myrecarray[2][1][0:10])
    
    # Create the label list for the major x ticks
    test_labels = []
    for i in range(len(x_axis_labels)):
        if i % 20 == 0:
            test_labels.append(x_axis_labels[i])
    
    # Personalize the Y axis ticks
    pos = N.arange(4)+0.5    # Center the points on the Y-axis ticks
    pylab.yticks(pos, y_axis_labels)
    
    # Transform the X axis ticks to reflect the time the sample was taken
    pos = N.arange(len(test_labels))
    pylab.xticks(pos, test_labels)
    
    # Set the graph limits (preferable to leave some space so it looks good)
    plt.ylim([0, 4])
    plt.xlim([1, points_limit])
    plt.plot(x, y, 'o')
    
    # Set major and minor ticks, here minor ticks are unlabelled
    majorLocator   = MultipleLocator(20)
    minorLocator   = MultipleLocator(5)
    ax.xaxis.set_major_locator(majorLocator)
    ax.xaxis.set_minor_locator(minorLocator)
    
    # -------------------------------- Show Graph ---------------------------- #
    print "done"
     
    fig.autofmt_xdate() 
    canvas=FigureCanvas(fig)
    response=HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response

