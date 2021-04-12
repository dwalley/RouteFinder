# random walk module for random walks in a cartesian world

from hexagon import *
from world import *
from pylab import *
import hexcontrol
import random
import numpy

class walk(hexagon):


    def __init__(self,hex_controler,my_world):
        self.places = []
        #list of hexagons visited on walk
        self.distances = []
        #lists of distances from the origin
        self.costs_list = []
        # list of costs incurred on walk
        self.benefits_list = []
        # list of benefits incurred on walk
        
        #start with a hexagon at the origin, oriented to the North
        n = len(hex_controler.roots)
##        print 'number of roots is',n
        self.origin = hex_controler.roots[n-1]
        self.places.append(self.origin)
        self.distances.append(0)
        self.costs_list.append(numpy.array((0.0,0.0,0.0)))
        self.benefits_list.append(numpy.array((0.0,0.0)))

    def go_on_walk(self,n):
        # build a random walk of n steps
        assert type(n) == type(1)
        assert n >= 1
        for i in range(0,n):
            n_adjacent = len(self.places[i].adjacent)
##            if  n_adjacent != 6:
##                print 'bouncing off wall'
            #choose a random direction
            r_index = random.choice(range(0,n_adjacent))
            temp_hexagon = self.places[i].adjacent[r_index]
            self.places.append(temp_hexagon)
            self.distances.append(self.origin.distance_between(self.origin.location,temp_hexagon.location))
##            print 'new cost is ',self.places[i].costs[r_index]
##            print 'previous accumulated cost is',self.costs_list[-1]
##            print 'appending to costs_list ',self.places[i].costs[r_index]+self.costs_list[-1]
            self.costs_list.append(self.places[i].costs[r_index]+self.costs_list[-1])
##            print 'appending to benefits list', self.places[i].benefit+self.benefits_list[-1]
            self.benefits_list.append(self.places[i].benefit+self.benefits_list[-1])


    def draw_walk(self):
        # draw the hexagons visited
        for i in range(0,len(self.places)):
            self.places[i].draw()
        #draw lines connecting centers of hexagons
        for i in range(1,len(self.places)):
            temp_line = line(self.places[i].location,self.places[i-1].location)
            temp_line.draw_line()
        # scale axes on window
        temp_max_distance = max(self.distances)
        # give a little extra room
        temp_max_distance = 1.1*temp_max_distance
        axis([((-640.0/480.0)*temp_max_distance),((640.0/480.0)*temp_max_distance),\
              (-1.0*temp_max_distance),temp_max_distance])


class collection_of_walks(walk):

    def __init__(self,hex_controler):
        self.walks = []
        self.average_distances = []
        self.average_costs = []
        self.average_benefits = []
        self.hex_controler = hex_controler

    def make_trials(self,num_trials,length_of_walks,my_world):
        #populates self.walks with num_trials of walks of length length_of_walks
        for i in range(0,num_trials):
            temp_walk = walk(self.hex_controler,my_world)
            temp_walk.go_on_walk(length_of_walks)
            self.walks.append(temp_walk)

    def calculate_average_distances(self):
        # makes a list of average distances of all the walks as a function of time
        # assumes all the walks are the same length
        length_of_walks = len(self.walks[0].distances)
        for i in range(0,length_of_walks):
            temp_total_distance = 0
            for w in self.walks:
                temp_total_distance += w.distances[i]
            self.average_distances.append(temp_total_distance/len(self.walks))
            
    def calculate_average_costs(self):
        # makes a list of average costs of all the walks as a function of time
        # assumes all the walks are the same length
        length_of_walks = len(self.walks[0].costs_list)
        for i in range(0,length_of_walks):
            temp_total_costs = numpy.array((0.0,0.0,0.0))
##            print 'temp_total_costs at top of loop is',temp_total_costs
            for w in self.walks:
                temp_total_costs += w.costs_list[i]
##            print 'temp_total_costs after accumulating across all walks is',temp_total_costs
##            print 'temp_total_costs/len(self.walks) is',temp_total_costs/len(self.walks)
            self.average_costs.append(temp_total_costs/len(self.walks))

    def calculate_average_benefits(self):
        # makes a list of average benefits of all the walks as a function of time
        # assumes all the walks are the same length
        length_of_walks = len(self.walks[0].benefits_list)
        for i in range(0,length_of_walks):
            temp_total_benefits = numpy.array((0.0,0.0))
            for w in self.walks:
                temp_total_benefits += w.benefits_list[i]
            self.average_benefits.append(temp_total_benefits/len(self.walks))

    def plot_distances(self):
        figure()
        num_trials = len(self.walks)
        length_of_walks = len(self.walks[0].distances)-1
        plot(self.average_distances)
        xlabel('Units of time')
        ylabel('Average Distance from Origin')
        title('Graph of Time versus Average Distance for '+str(num_trials)+' random walks of length '+str(length_of_walks))
        
    def plot_costs(self):
        figure()
        num_trials = len(self.walks)
        length_of_walks = len(self.walks[0].distances)-1
        plot(self.average_costs)
        xlabel('Units of time')
        ylabel('Average Costs')
        title('Graph of Time versus Average Costs for '+str(num_trials)+' random walks of length '+str(length_of_walks))
        
    def plot_benefits(self):
        figure()
        num_trials = len(self.walks)
        length_of_walks = len(self.walks[0].distances)-1
        plot(self.average_benefits)
        xlabel('Units of time')
        ylabel('Average Benefits')
        title('Graph of Time versus Average Benefits for '+str(num_trials)+' random walks of length '+str(length_of_walks))
        
    def scatterplot_final_locations(self):
        figure()
        xlocs = []
        ylocs = []
        length_of_walk = len(self.walks[0].distances)
        for w in self.walks:
            xlocs.append(w.places[length_of_walk-1].location.x1)
            ylocs.append(w.places[length_of_walk-1].location.x2)
        scatter(xlocs,ylocs)
        xlabel('X location')
        ylabel('Y location')
        title('Scatter plot of final locations for '+str(num_trials)+' random walks of length '+str(length_of_walks))
        
    def histogram_final_locations(self):
        figure()
        xlocs = []
        ylocs = []
        length_of_walk = len(self.walks[0].distances)-1
        for w in self.walks:
            xlocs.append(w.places[length_of_walk].location.x1)
            ylocs.append(w.places[length_of_walk].location.x2)
        hist(xlocs,10)
        xlabel('Final X locations')
        ylabel('Number of walks')
        title('Histogram of final X locations for '+str(num_trials)+' random walks of length '+str(length_of_walks))
        figure()
        hist(ylocs,10)
        xlabel('Final Y locations')
        ylabel('Number of walks')
        title('Histogram of final Y locations for '+str(num_trials)+' random walks of length '+str(length_of_walks))
        
    def histogram_final_distances(self):
        figure()
        length_of_walks = len(self.walks[0].distances) - 1
        final_distances = []
        for w in self.walks:
            final_distances.append(w.distances[length_of_walks])
        temp_total = 0
        for i in final_distances:
            temp_total +=i
        average_final_distance = temp_total/len(final_distances)
        hist(final_distances,10)
        axvline(average_final_distance)
        xlabel('Final distances')
        ylabel('Number of walks')
        title('Histogram of final distances for '+str(num_trials)+' random walks of length '+str(length_of_walks))
        
        
print 'done initializing.  starting computations'

# initialize world
my_world=world()

#read in hex tree file with cost/benefit data
file_name = 'testout1.txt'
print 'reading hex tree from',file_name
# make a temporary root hex
bootstrap_hex = hexagon(0,0,0,0,my_world)
hex_controler = hexcontrol.hexcontrol(bootstrap_hex,my_world)
# load the stored dictionary into the root's dictionary, making hexs for each dictionary entry
test_hex = hex_controler.read_dictionary(file_name,my_world)
n = test_hex.depth()
print 'done reading hex tree, depth of tree is',n

#create collection of walks
c = collection_of_walks(hex_controler)

num_trials = 400
length_of_walks = 500

print 'making trials'
c.make_trials(num_trials,length_of_walks,my_world)

print 'calculating average distances'
c.calculate_average_distances()

#plot out the average distances as a function of time
print 'drawing distances plot'
c.plot_distances()

print 'calculating average costs'
c.calculate_average_costs()

#plot out the average costs as a function of time
print 'drawing costs plot'
c.plot_costs()

print 'calculating average benefits'
c.calculate_average_benefits()

#plot out the average benefits as a function of time
print 'drawing benefits plot'
c.plot_benefits()

#scatter plot of final locations
print 'making scatter plot'
c.scatterplot_final_locations()

#histograms of final x and y locations
print 'making location histograms'
c.histogram_final_locations()

#histograms of final distances
print 'making final distances histogram'
c.histogram_final_distances()

# display some walks
figure()
print 'drawing walks'
c.walks[0].draw_walk()
xlabel('Abcissa')
ylabel('Ordinate')
title('First Random Walk')

figure()
c.walks[1].draw_walk()
xlabel('Abcissa')
ylabel('Ordinate')
title('Second Random Walk')

show()
