import math
import time
import matplotlib.pyplot as plt
import numpy
import pylab

# population dynamics

alpha = 0.0003 #growth rate of prey
gamma = 0.0009 #death rate of predator
beta = 0.0005 #effect of predator on prey
kappa = 0.0007 #effect of prey on predator

# prey, predator initial populations
y_0 = 250
a_0 = 30
max_time = 100

# population list for prey (y) and predator (a)
prey = []
predator = []

# define time
t = 0
a = a_0
y = y_0
##plt.xlim(0,max_time)
##plt.ylim(0,300)
pylab.xlim(0,max_time)
pylab.ylim(0,y_0+100)

y_prey = numpy.array([])
y_predator = numpy.array([])
time_pd = numpy.array([])
t = 0

while t < max_time:
    y = y_0*math.exp((alpha-beta*a)*t)
    a = a_0*math.exp((kappa*y-gamma)*t)
    y_prey = numpy.append(y_prey,y)
    y_predator = numpy.append(y_predator,a)
    time_pd = numpy.append(time_pd,t)
##    prey_plt = plt.plot(prey)
##    predator_plt = plt.plot(predator)
##    plt.pause(0.001)
##    plt.draw()
    
    pylab.plot(time_pd,y_prey,'b',label='prey')
    pylab.plot(time_pd,y_predator,'r',label='predator')
    t+=1
pylab.show()
