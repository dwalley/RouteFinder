## hexcontrol is a class whose objects have methods for working with a completed hex tree

from __future__ import print_function

import world
import fileinput
import hexagon
import world
import math
import pylab
import os
import random
import numpy


class hexcontrol:

    def __init__(self,hexagon,my_world):
        self.source_hex = hexagon.get_root()
        self.roots = []
        self.my_world = my_world
        self.lowest_center_hex = self.source_hex
        while self.lowest_center_hex.children != []:
            self.lowest_center_hex = self.lowest_center_hex.children[0]
        if self.lowest_center_hex != self.source_hex: # we have a non-empty tree
            
            self.sort_adjacent_hexs()

            # calculate the convex hull of lowest hexagon field
            self.convex_hull = []
            for i in range(0,6): # go in each of the six directions from the center lowest hex
                temp_hex = self.lowest_center_hex
                self.convex_hull_count = 0
                while len(temp_hex.adjacent) == 6: # we have not reached the edge of the hex field
                    self.convex_hull_count += 1
                    temp_hex = temp_hex.adjacent[i]
                self.convex_hull.append(temp_hex.location)
            self.convex_hull_outside_diameter = my_world.distance_between(self.convex_hull[0],self.convex_hull[3])
            
            #update the field of view of my_world to hold hex field
            my_world.x1_lower_limit = self.source_hex.location.x1 - (1600.0/1080.0)*2.0*self.convex_hull_outside_diameter/2
            my_world.x1_upper_limit = self.source_hex.location.x1 + (1600.0/1080.0)*2.0*self.convex_hull_outside_diameter/2
            my_world.x2_lower_limit = self.source_hex.location.x1 - 2.0*self.convex_hull_outside_diameter/2
            my_world.x2_upper_limit = self.source_hex.location.x1 + 2.0*self.convex_hull_outside_diameter/2

    def change_scale(self,new_outside_diameter):
        ###change scale of entire hex field so outside diameter of source hex matches new_outside_diameter ###
        if not(new_outside_diameter > 0):
            raise badOutsideDiameter
        if self.roots == []:
            self.find_roots()
        scale_factor = new_outside_diameter/self.source_hex.outside_diameter
        # go through all the hexagons at each level of the tree and update their locations.
        for temp_root_hex in self.roots:
            for temp_key,temp1_hex in temp_root_hex.hexagon_dictionary.items():
                #make a line from the center of the hex field to our current hexagon
                temp_line = world.line(self.source_hex.location,temp1_hex.location)
                # calculate new point along ray properly scaled
                temp1_hex.location = temp_line.along_line(temp_line,scale_factor)
                # change the outside diameter for our current hexagon
                temp1_hex.outside_diameter = temp1_hex.outside_diameter * scale_factor
        # update the locations for the convex hull
        for i in range(0,len(self.convex_hull)):
            #make a line from the center of the hex field to our current convex hull 
            temp_line = world.line(self.source_hex.location,self.convex_hull[i])
            # make end of the line the new location for our current hexagon
            self.convex_hull[i] = temp_line.along_line(temp_line,scale_factor)
        
        return True

    def change_orientation(self,new_orientation):
        ###rotate entire hex field so that orientation of source hex points in direction of new_orientation ###
        if not((new_orientation >= 0) and (new_orientation <= 360)):
            raise badOrientation
        if self.roots == []:
            self.find_roots()
        delta_orientation = (new_orientation - self.source_hex.orientation)%360
        # go through all the hexagons at each level of the tree and update their locations.
        for temp_root_hex in self.roots:
            for temp_key,temp1_hex in temp_root_hex.hexagon_dictionary.items():
                #make a line from the center of the hex field to our current hexagon
                temp_line = world.line(self.source_hex.location,temp1_hex.location)
                # rotate said line about the center of the hex field
                temp_line = temp_line.rotate_line(temp_line,delta_orientation)
                # make end of the line the new location for our current hexagon
                temp1_hex.location = temp_line.p2
                # change the orientation for our current hexagon
                temp1_hex.orientation = (temp1_hex.orientation + delta_orientation) % 360
        # update the locations for the convex hull
        for i in range(0,len(self.convex_hull)):
            #make a line from the center of the hex field to our current convex hull 
            temp_line = world.line(self.source_hex.location,self.convex_hull[i])
            # rotate said line about the center of the hex field
            temp_line = temp_line.rotate_line(temp_line,delta_orientation)
            # make end of the line the new location for our current hexagon
            self.convex_hull[i] = temp_line.p2
        
        return True

    def translate_hex_field(self,new_location):
        ### translates entire hex field to be centered at new_location ###
        # assumes self is a properly initialized hex controller
        if type(new_location) != type(world.location(0,0)):
            raise badLocation
        if self.roots == []:
            self.find_roots()
##        print('IN translate_hex_field')
##        print('number of roots is'+str(len(self.roots)))
        delta_location = new_location.subtract(self.source_hex.location)
##        print('new_location is'+str(new_location)+' and delta_location is'+str(delta_location))
        # go through all the hexagons at each level of the tree and update their locations.
        for temp_root_hex in self.roots:
            for temp_key,temp1_hex in temp_root_hex.hexagon_dictionary.items():
                temp1_hex.location = temp1_hex.location.add(delta_location)
        # update the locations for the convex hull
        for i in range(0,len(self.convex_hull)):
            self.convex_hull[i] = self.convex_hull[i].add(delta_location)
        #update the field of view of my_world to hold hex field
        self.my_world.x1_lower_limit = self.source_hex.location.x1 - (640.0/480.0)*1.1*self.convex_hull_outside_diameter/2
        self.my_world.x1_upper_limit = self.source_hex.location.x1 + (640.0/480.0)*1.1*self.convex_hull_outside_diameter/2
        self.my_world.x2_lower_limit = self.source_hex.location.x1 - 1.1*self.convex_hull_outside_diameter/2
        self.my_world.x2_upper_limit = self.source_hex.location.x1 + 1.1*self.convex_hull_outside_diameter/2
        
        return True
        

    def line_of_hexagons(self,p_start,p_end,use_convex_hull = True):
        ### generator for a iterator which returns hexagons which from line from p_start to p_end ###
        # Note: p_start must be within the hexagon field
        # guarantees that first hex contains p_start and last hex contains p_end or else p_end is off the field
##        print('line of hexagons called with use_convex_hull = '+str(use_convex_hull))
        current_hex = self.lowest_hex_containing_point(p_start,use_convex_hull)
##        print('starting hex location is '+str(current_hex.location))
        reference_line = world.line(current_hex.location,p_end)
##        print('reference line is '+str(reference_line))
        current_distance = current_hex.distance_between(current_hex.location,p_end)
        yield current_hex
        for temp_hex in current_hex.adjacent:
            if temp_hex.line_intersects(reference_line):
                current_hex = temp_hex
                current_distance = current_hex.distance_between(current_hex.location,p_end)
                break
        else: # none of and adjacents have the reference line crossing them, we are done
            return
        yield current_hex
        while current_hex.is_interior(p_end) != True and len(current_hex.adjacent) == 6:
            # zigzag across reference line until we get there, stopping when we get to p_end or reach the edge
            candidate_hexs = []
            for temp_hex in current_hex.adjacent: # see which adjacent hexs are on other side of reference line
                temp_line = world.line(current_hex.location,temp_hex.location)
                if temp_hex.segments_intersect(p_start,p_end,current_hex.location,temp_hex.location):
                    # we found an adjacent hex on the other side of the reference line
                    candidate_hexs.append(temp_hex)
            if candidate_hexs == []: # we did not find any hexs on the other side of the reference line
                return
            else:
                old_current_hex = current_hex
                for temp_hex in candidate_hexs:
                    if temp_hex.distance_between(temp_hex.location,p_end) < current_distance:
                        current_hex = temp_hex
                        current_distance = temp_hex.distance_between(temp_hex.location,p_end)
                if old_current_hex == current_hex: # none of the candidate hexs are better than before
                    return
            yield current_hex
        # when we get this far, current_hex contains p_end
        return

    def lowest_hex_containing_point(self,p,use_convex_hull=True):
        ### returns leaf hexagon containing point p, p must be within the original root hexagon ###
##        print(' ')
##        print('in method lowest_hex_containing_point')
##        print('point is '+str(p))
##        print('use_convex_hull is '+str(use_convex_hull))
##        print('within_convex_hull is '+str(self.my_world.within_convex_hull(p,self.convex_hull)))
        if use_convex_hull and self.my_world.within_convex_hull(p,self.convex_hull) != True:
            raise locationNotInWorld
        else:
            current_hex = self.source_hex #points to the hex whose children are examined for containing p
            for i in range(0,self.source_hex.depth()): # go through levels of hexagon tree, stopping one above bottom
##                print('depth in tree is '+str(i))
                temp_counter = -1
                for temp_hex in current_hex.children:
                    temp_counter += 1
##                    print('looking at child number '+str(temp_counter))
                    if temp_hex.is_interior(p) == True: # we found the child hex containing the point
##                        print('p is interior to hexagon at '+str(temp_hex.location))
##                        print('hexagon diameter is '+str(temp_hex.outside_diameter))
                        current_hex = temp_hex
                        break
                else:
                    # We did not find a child hex containing the point
                    # Either there was a rounding error or we are within the convex hull of the lowest level
                    # but not in a hex at this level.  Find the closest hex from among the children
                    temp_hex = current_hex.children[0]
                    temp_distance = temp_hex.distance_between(temp_hex.location,p)
                    for other_hex in current_hex.children[1:]:
                        if temp_hex.distance_between(p,other_hex.location) < temp_distance:
                            temp_hex = other_hex
                            temp_distance = temp_hex.distance_between(temp_hex.location,other_hex.location)
##                    print('temp_hex location is '+str(temp_hex.location))
                    current_hex = temp_hex

            return current_hex

    def generate_random_costs(self):
        ### populate costs and benefits to the lowest level randomly, 3 costs and 2 benefits per ###
        # costs is a list of 3 costs for going from each adjacent on the adjacent list to the current hex
        # benefits is a list of 2 benefits for arriving at the current hex
        temp_hex = self.source_hex
##        print('depth of tree is '+str(self.source_hex.depth()))
        for i in range(0,self.source_hex.depth()+1): # go through levels of hexagon tree
            print('generating random costs and benefits for level '+str(i))
            for temp_key,temp1_hex in temp_hex.get_center().hexagon_dictionary.items():
                temp1_hex.costs = [[random.random(),random.random(),random.random()] for j in temp1_hex.adjacent]
                # temp1_hex.benefit = [random.random(),random.random()]
                temp1_hex.benefit = [0.0,0.0]
            if i < self.source_hex.depth():
##                print('depth of tree is '+str(self.source_hex.depth()))
                temp_hex = temp_hex.children[0] # make it point to the center hex of the next level


    def sort_adjacent_hexs(self):
        ###goes through completed tree doing clockwise sorting of adjacent hexs lists ###
        temp_hex = self.source_hex
        for i in range(0,self.source_hex.depth()+1): # go through levels of hexagon tree
            for temp_key,temp1_hex in temp_hex.get_center().hexagon_dictionary.items():
                temp1_hex.sort_adjacent()
            if i != self.source_hex.depth():
                temp_hex = temp_hex.children[0] # make it point to the center hex of the next level

    def check_children(self):
        temp_hex = self.source_hex
        for i in range(0,self.source_hex.depth()+1): # go through levels of hexagon tree
            for temp_key in temp_hex.get_center().hexagon_dictionary: #iterate through the dictionary for that level
                temp1_hex = temp_hex.get_center().hexagon_dictionary[temp_key]
                if len(temp1_hex.children) != 0 and len(temp1_hex.children) != 7: #Houston, we have a problem
                    print('temp_hex number of children is'+str(len(temp1_hex.children)))
                    print('depth of hex is'+str(temp1_hex.height()))
                    print('key is '+str(temp1_hex.key))
                    print(str(temp1_hex.children))
            if i != self.source_hex.depth():
                temp_hex = temp_hex.children[0] # make it point to the center hex of the next level

    def compare_centers(self):
        # makes a list distances between locations for every pair of hexs in the dictionary at current and lower levels
        temp_hex = self.source_hex
        temp_list = []
        for i in range(0,self.source_hex.depth()+1): # go through sublevels of hexagon tree
            center_hex = temp_hex.get_center()
            for temp1_key in center_hex.hexagon_dictionary: #iterate through the dictionary for that level
                for temp2_key in center_hex.hexagon_dictionary: #looking at all pairs
                    if temp1_key != temp2_key:
                        temp1_hex = center_hex.hexagon_dictionary[temp1_key]
                        temp2_hex = center_hex.hexagon_dictionary[temp2_key]
                        temp_list.append((temp1_key,temp2_key,\
                                          math.sqrt((temp1_hex.location.x1 - temp2_hex.location.x1)**2 +\
                                                    (temp1_hex.location.x2 - temp2_hex.location.x2)**2)))
            if i != self.source_hex.depth():
                temp_hex = temp_hex.children[0] # make it point to the center hex of the next level
        return temp_list

    def find_roots(self):
        temp_hex = self.source_hex
        tree_depth = self.source_hex.depth()
        self.roots = []
        for i in range(0,tree_depth+1):
            self.roots.append(temp_hex.get_center())
            if i != tree_depth:
                temp_hex = temp_hex.children[0].get_center()
        return None

    def arrayize_costs_benefits(self):
        ###convert cost and benefit lists into arrays ###
        self.find_roots()
        tree_depth = len(self.roots)
        for i in range(0,tree_depth):
            for temp_key in self.roots[i].hexagon_dictionary:
                temp_hex = self.roots[i].hexagon_dictionary[temp_key]
                temp_hex.costs = [numpy.array(temp) for temp in temp_hex.costs]
                temp_hex.benefit = numpy.array(temp_hex.benefit)

    def keyize_pointers(self,my_world):
        #convert all references to other hexagons into keys, breaking links betweens
        # returns list of root hexagons so that we can continue to work with the tree as a whole
        self.find_roots()
        tree_depth = len(self.roots)
        for i in range(0,tree_depth): # go through levels of hexagon tree
            for temp1_key in self.roots[i].hexagon_dictionary:
                #iterate through the dictionary for that level
                temp1_hex = self.roots[i].hexagon_dictionary[temp1_key]
                temp_len = len(temp1_hex.parents)
                for j in range(0,temp_len): # convert parents list to list of dictionary keys
                    temp1_hex.parents[j] = temp1_hex.parents[j].key
                temp_len = len(temp1_hex.children)
                for j in range(0,temp_len): # convert children list to list of dictionary keys
                    temp1_hex.children[j] = temp1_hex.children[j].key
                temp_len = len(temp1_hex.adjacent)
                for j in range(0,temp_len): # convert adjacent list to list of dictionary keys
                    temp1_hex.adjacent[j] = temp1_hex.adjacent[j].key
        return None

    def unkeyize_pointers(self):
        #convert all references to other hexagons into object references
        #num_parents = []
        #num_children = []
        #num_adjacent = []
        for level in range(0,len(self.roots)):
            for temp_key in self.roots[level].hexagon_dictionary:
                temp1_hex = self.roots[level].hexagon_dictionary[temp_key]
                if level > 0:
                    temp_len = len(temp1_hex.parents)
                    for i in range(0,temp_len): # convert parents keys to list of hex pointers
                        try:
                            temp1_hex.parents[i] = self.roots[level-1].hexagon_dictionary\
                                [temp1_hex.parents[i]]
                        except:
                            print('i ',i,'level - 1 ',level-1,'temp1_hex.parents[i] ',\
                                temp1_hex.parents[i])
                            raise hell
                    #num_parents.append(temp_len)
                if level < len(self.roots):
                    temp_len = len(temp1_hex.children)
                    for i in range(0,temp_len): # convert children keys to list of hex pointers
                        temp1_hex.children[i] = self.roots[level+1].hexagon_dictionary[temp1_hex.children[i]]
                    #num_children.append(temp_len)
                temp_len = len(temp1_hex.adjacent)
                for i in range(0,temp_len): # convert adjacent keys to list of hex pointers
                    temp1_hex.adjacent[i] = self.roots[level].hexagon_dictionary[temp1_hex.adjacent[i]]
                #num_adjacent.append(temp_len)
                
        #pylab.hist(num_parents,bins=5)
        #pylab.title('Parents Histogram')
        #pylab.figure()
        #pylab.hist(num_children,bins=8)
        #pylab.title('Children Histogram')
        #pylab.figure()
        #pylab.hist(num_adjacent,bins=7)
        #pylab.title('Adjacent Histogram')
        #pylab.figure()
        #pylab.show()
        return None

    
    def save_hex_tree(self,file_name,my_world):
        #open the file
        #save all the hexs in the tree and close the file.
        f=open(file_name,'w')
        self.keyize_pointers(my_world)
        for level in range(0,len(self.roots)):
            for temp_key in self.roots[level].hexagon_dictionary:
                temp_hex = self.roots[level].hexagon_dictionary[temp_key]
                print (temp_key,file=f)
                print(temp_hex.location,file=f)
                print(temp_hex.outside_diameter,file=f)
                print(temp_hex.orientation,file=f)
                print(temp_hex.parents,file=f)
                print(temp_hex.children,file=f)
                print(temp_hex.adjacent,file=f)
                print(temp_hex.costs,file=f)
                print(temp_hex.benefit,file=f)
        f.close()
        self.unkeyize_pointers()

    def read_dictionary(self,file_name,my_world):
        # reads a  file and builds a hexagon tree for root hex using keys
        # assumes that the hex's in the file were put in breadth first order
        # root hex will need additional processing to be made into a full hex tree
        line_no = 0
        self.roots = []
        current_level = -1
        num_parents = []
        num_children = []
        num_adjacent = []
        #print(str(os.getcwd())+' is the current working directory')
        f=open(file_name,'r')
        for line in f:
            temp_line = line
            #print(temp_line)
            x=eval(temp_line)
            if line_no == 0:# we a reading in data for a new hex, starting with the key
                #print('starting new hex')
                temp_hex = hexagon.hexagon(0,0,0,0,my_world) #make a new hexagon
                temp_hex.key = x
                if len(temp_hex.key)-1 > current_level: # we are starting to read hex's from the next level
                    # set up this hex as a temporary root hex until we come across the real root
                    current_level +=1
                    self.roots.append(temp_hex)
                    self.roots[current_level].hexagon_dictionary = {}
                    current_root_hex = temp_hex 
                # check to see if this is the real root hex for the next level
                # that is, it has all 0's for a key
                might_be_root = True
                for i in range(0,len(temp_hex.key)):
                    if temp_hex.key[i] != 0:
                        might_be_root = False
                # if might_be_root is still true, this is the level root hex for the current level
                if might_be_root == True:
                    # move the level dictionary over to this hexagon
                    temp_hex.hexagon_dictionary = current_root_hex.hexagon_dictionary
                    # fix the roots to point to this hex
                    self.roots[current_level] = temp_hex
                    # change current_root_hex to point to this new hex
                    current_root_hex = temp_hex
            elif line_no == 1:# location as a tuple
                temp_hex.location.x1 , temp_hex.location.x2 = x
            elif line_no == 2:# outside diameter
                temp_hex.outside_diameter = x
            elif line_no == 3:#orientation
                temp_hex.orientation = x
            elif line_no == 4:#parent list as list of keys
                temp_hex.parents = x
                num_parents.append(len(x))
            elif line_no == 5: #children list as list of keys
                temp_hex.children = x
                num_children.append(len(x))
            elif line_no == 6: # adjacent list as list of keys
                temp_hex.adjacent = x
                num_adjacent.append(len(x))
            elif line_no == 7: #costs list
                temp_hex.costs = x
            elif line_no == 8: # line_no == 8, benefit
                temp_hex.benefit = x
                # we now have all the basic pieces in temp_hex, update the dictionary
                current_root_hex.hexagon_dictionary[temp_hex.key]=temp_hex
                #print('last line of a hexagon')
                
            if line_no == 8:
                line_no = 0
            else:
                line_no +=1
                
        ## we are done reading in from file
        #pylab.hist(num_parents,bins=5)
        #pylab.title('Parents Histogram')
        #pylab.figure()
        #pylab.hist(num_children,bins=8)
        #pylab.title('Children Histogram')
        #pylab.figure()
        #pylab.hist(num_adjacent,bins=7)
        #pylab.title('Adjacent Histogram')
        #pylab.figure()
        #pylab.show()

        #for i in range(0,len(self.roots)):
        #    print('Level '+str(i)+' Root key is')
        #    print(str(self.roots[i].key))
        #    print('Size of Level Dictionary is')
        #    print(str(len(self.roots[i].hexagon_dictionary)))
        #    print(self.roots[i].hexagon_dictionary)
            #for tempKey in self.roots[i].hexagon_dictionary.keys():
            #    tempHex = self.roots[i].hexagon_dictionary[tempKey]
            #    print(tempKey,tempHex,tempHex.parents,tempHex.adjacent,tempHex.children)
        # we should now have recreated the hexagon tree with root_hex as the root but
        # with all parent, child, and adjacent relationships in the form of keys
        
        self.unkeyize_pointers()

        self.source_hex = self.roots[0]

        self.arrayize_costs_benefits()

##        print('depth of newly read in tree is '+str(self.source_hex.depth()))

        # self.source_hex should now point to a valid recreation of the original hex tree

        f.close()
        
        return self.roots[0]
        
