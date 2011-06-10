from django.shortcuts import render_to_response
import dot_chart
from django.http import HttpResponse
import numpy as N
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from dateutil import parser
import pylab
import time

def visuals(request):
   # f = open('mobility_sample.csv', 'r')
   # dot_chart.plot_chart('mobility_sample.csv')
  # img = test1.simple 
   img = "hello"
   return render_to_response('mobvisuals/visuals.html', {'image': img})
  # return HttpResponse("Mobvisuals Index")

def index(request):
    return HttpResponse("My Dashboard")

def Login(request):
    campaign = "Mobilize"
    return render_to_response('mobvisuals/Login.html', {'campaign_name': campaign})

def py_dot_chart(request):
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
    myrecarray = dot_chart.read_array('mobility_sample.csv', descr)

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
            temp = dot_chart.det_majority((myrecarray[7])[i:array_len], y_axis_labels)
            mean_time = dot_chart.det_mean((myrecarray[2])[i:array_len])
        else:
            temp = dot_chart.det_majority((myrecarray[7])[i:i+grouping], y_axis_labels)
            mean_time = dot_chart.det_mean((myrecarray[2])[i:i+grouping])
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
    fig = plt.figure()
    ax = plt.subplot(111)
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
