# world module, contains methods for working with points and lines
# encapsulates destinction between Cartesian and Spherical worlds

import numpy


import math
from pylab import *
import random

class world:
    #cartesian or polar, cartesian for now, requires an instantiation named my_world prior to use of methods

    def __init__(self):
        global type_world
        type_world = 'cartesian'
        self.type_world = 'cartesian'
        # aspect ratios used in drawing on a computer screen
        self.x1_lower_limit = -640
        self.x1_upper_limit =  640
        self.x2_lower_limit = -480
        self.x2_upper_limit =  640
        # accuracy_factor is chosen to give 10 meter accuracy anywhere on the globe when using lat/longs
        self.accuracy_factor = 359251200

    def within_convex_hull(self,p,vertex_list):
        ### returns true if location p is inclusively within the polygon defined by vertex list ###
        # note vertex list must be a sequential list of vertices of a convex polygon in clockwise order
##        print 'vertex list for convex hull is',vertex_list
        for i in range(1,len(vertex_list)):
            temp_direction = self.direction(vertex_list[i-1],vertex_list[i],p)
            if temp_direction < 0:
                return False
        if self.direction(vertex_list[-1],vertex_list[0],p) < 0:
            return False
        else:
            return True

    def proper_lines_intersect(self,line1,line2):
        ### returns true if line1 and line 2 intersect in their interiors ###
        assert type(line1) == type(line(location(0,0),location(1,1)))
        assert type(line2) == type(line(location(0,0),location(1,1)))

        d1 = self.direction(line2.p1,line2.p2,line1.p1)
        d2 = self.direction(line2.p1,line2.p2,line1.p2)
        d3 = self.direction(line1.p1,line1.p2,line2.p1)
        d4 = self.direction(line1.p1,line1.p2,line2.p2)
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and\
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        else:
            return False

    def on_segment(self,pi,pj,pk):
        ### returns true if pk is inclusively between the endpoints of segment pi->pj ###
        if self.direction(pi,pj,pk) == 0:
            if min(pi.x1,pj.x1) <= pk.x1 and pk.x1 <= max(pi.x1,pj.x1) and\
               min(pi.x2,pj.x2) <= pk.x2 and pk.x2 <= max(pi.x2,pj.x2):
                return True
            else:
                return False
        else:
            return False

    def segments_intersect(self,p1,p2,p3,p4):
        ### returns true is segment from p1 to p2 intersects segment from p3 to p4 ###
        assert type(p1) == type(location(0,0))
        assert type(p2) == type(location(0,0))
        assert type(p3) == type(location(0,0))
        assert type(p4) == type(location(0,0))

        def on_segment(pi,pj,pk):
            if min(pi.x1,pj.x1) <= pk.x1 and pk.x1 <= max(pi.x1,pj.x1) and\
               min(pi.x2,pj.x2) <= pk.x2 and pk.x2 <= max(pi.x2,pj.x2):
                return True
            else:
                return False
        
        d1 = self.direction(p3,p4,p1)
        d2 = self.direction(p3,p4,p2)
        d3 = self.direction(p1,p2,p3)
        d4 = self.direction(p1,p2,p4)
        if ((d1 > 0 and d2 < 0) or (d1 < 0 and d2 > 0)) and\
           ((d3 > 0 and d4 < 0) or (d3 < 0 and d4 > 0)):
            return True
        elif d1 == 0 and on_segment(p3,p4,p1):
            return True
        elif d2 == 0 and on_segment(p3,p4,p2):
            return True
        elif d3 == 0 and on_segment(p1,p2,p3):
            return True
        elif d4 == 0 and on_segment(p1,p2,p4):
            return True
        else:
            return False

    def sort_segments(self,p0,q,plist,direction = 'clockwise'):
        ### sorts plist in place in order of direction with p0->q being the reference segment ###
        # each item in plist must have a location, returns permuted list of new locations for reference
        assert type(p0) == type(location(0,0))
        assert type(q) == type(location(0,0))
        assert type(plist) == type([])

        permuted_list = list(range(0,len(plist)))

        if plist == []:
            return None
        elif direction == 'counterclockwise':
##            print 'doing CCW sort'
            start = 0
            end = len(plist)-1
            working_stack = [(start,end)]
            max_working_stack = 1
            first_time = True
            while len(working_stack) != 0:
##                print [(i.x1,i.x2) for i in plist]
                # note that the first time thru we pivot about -(p0->q) 
                start,end = working_stack.pop()
                #handle some trivial cases
                if start >= end: #at most one element list, no sorting to do
                    pass
                elif end-start == 1:# we have a 2 element list
                    if self.direction(p0,plist[start].location,plist[end].location) < 0: # already in CCW order
                        pass
                    else: # points are in clockwise order, switch them
                        temp = plist[end]
                        plist[end]=plist[start]
                        plist[start]=temp
                        temp = permuted_list[end]
                        permuted_list[end]=permuted_list[start]
                        permuted_list[start]=temp
                    if first_time == True: # we need to see where q fits in
                        if self.direction(p0,plist[start].location,q) < 0 and\
                           self.direction(p0,q,plist[end].location) <= 0:
                            # q is between points or colinear with second point
                            # swap the points, otherwise we are OK
                            temp = plist[end]
                            plist[end]=plist[start]
                            plist[start]=temp
                            temp = permuted_list[end]
                            permuted_list[end]=permuted_list[start]
                            permuted_list[start]=temp
                else: # we have at least a 3 element list to work with
                    if first_time == True:
                        pivot = self.opposite(p0,q)
                    else:
                        #pick a random pivot
                        pivot_index = random.randint(start,end) #start + (start-end)/2
                        #switch the pivot with the head of the list
                        pivot = plist[pivot_index].location
                        pivot_item = plist[pivot_index]
                        plist[pivot_index]=plist[start]
                        plist[start]=pivot_item
                        temp= permuted_list[pivot_index]
                        permuted_list[pivot_index]=permuted_list[start]
                        permuted_list[start] = temp
                    #go through list making two sublists, the first consisting of all elements clockwise to pivot,
                    # the second consisting of elements CCW to pivot
                    if first_time == True:
                        i = start
                        j = start
                    else:
                        i=start + 1 # points to the start of the list CCW to pivot
                        j=start + 1 # index over the length of the list
                    while j <= end:
                        if self.direction(p0,pivot,plist[j].location) < 0: # element is CCW to pivot
                            j +=1
                        else:# it is clockwise or colinear to pivot, swap it into the left side and increment 
                            temp = plist[j]
                            plist[j] = plist[i]
                            plist[i]=temp 
                            temp = permuted_list[j]
                            permuted_list[j] = permuted_list[i]
                            permuted_list[i]=temp
                            i+=1
                            j+=1
                    if first_time == True:
                        #recursively sort the two sublists
                        if (i-1)-start > 0:
                            working_stack.append((start,i-1))
                        if end - i > 0:
                            working_stack.append((i,end))
                        first_time = False
                    else:
                        #we now have a list of the form [pivot, stuff clockwise pivot, stuff CCW pivot]
                        #swap pivot into the middle of the list forming [stuff <= pivot, pivot, stuff>pivot]
                        
                        plist[start] = plist[i-1]
                        plist[i-1] = pivot_item
                        temp = permuted_list[i-1]
                        permuted_list[i-1] = permuted_list[0]
                        permuted_list[0]=temp
                        #recursively sort the two sublists
                        if (i-2)-start > 0:
                            working_stack.append((start,i-2))
                        if end - i > 0:
                            working_stack.append((i,end))
            # having dropped through the while loop, we now have plist sorted in CCW order 
            # relative to p0->q with points pi s.t. p0->pi is colinear with p0->q are at the head of the list
        else: # we will sort clockwise
##            print 'doing clockwise sort'
            start = 0
            end = len(plist)-1
            working_stack = [(start,end)]
            max_working_stack = 1
            first_time = True
            while len(working_stack) != 0:
##                print [(i.x1,i.x2) for i in plist]
                # note that the first time thru we pivot about -(p0->q) 
                start,end = working_stack.pop()
                #handle some trivial cases
                if start >= end: #at most one element list, no sorting to do
                    pass
                elif end-start == 1:# we have a 2 element list
                    if self.direction(p0,plist[start].location,plist[end].location) > 0: # already in clockwise order
                        pass
                    else: # points are in counterclockwise order, switch them
                        temp = plist[end]
                        plist[end]=plist[start]
                        plist[start]=temp
                        temp = permuted_list[end]
                        permuted_list[end]=permuted_list[start]
                        permuted_list[start]=temp
                    if first_time == True: # we need to see where q fits in
                        if self.direction(p0,plist[start].location,q) > 0 and\
                           self.direction(p0,q,plist[end].location) >= 0: # q is between points or colinear with second point
                            # swap the points, otherwise we are OK
                            temp = plist[end]
                            plist[end]=plist[start]
                            plist[start]=temp
                            temp = permuted_list[end]
                            permuted_list[end]=permuted_list[start]
                            permuted_list[start]=temp
                else: # we have at least a 3 element list to work with
                    if first_time == True:
                        pivot = self.opposite(p0,q)
                    else:
                        #pick a random pivot
                        pivot_index = random.randint(start,end)#start + (start-end)/2
                        #switch the pivot with the head of the list
                        pivot = plist[pivot_index].location
                        pivot_item = plist[pivot_index]
                        plist[pivot_index]=plist[start]
                        plist[start]=pivot_item
                        temp= permuted_list[pivot_index]
                        permuted_list[pivot_index]=permuted_list[start]
                        permuted_list[start] = temp
                    #go through list making two sublists, the first consisting of all elements counterclockwise to pivot,
                    # the second consisting of elements clockwise to pivot
                    if first_time == True:
                        i = start
                        j = start
                    else:
                        i=start + 1 # points to the start of the list clockwise to pivot
                        j=start + 1 # index over the length of the list
                    while j <= end:
                        if self.direction(p0,pivot,plist[j].location) > 0: # element is clockwise to pivot
                            j +=1
                        else:# it is counterclockwise or colinear to pivot, swap it into the left side and increment 
                            temp = plist[j]
                            plist[j] = plist[i]
                            plist[i]=temp
                            temp = permuted_list[j]
                            permuted_list[j] = permuted_list[i]
                            permuted_list[i]=temp
                            i+=1
                            j+=1
                    if first_time == True:
                        #recursively sort the two sublists
                        if (i-1)-start > 0:
                            working_stack.append((start,i-1))
                        if end - i > 0:
                            working_stack.append((i,end))
                        first_time = False
                    else:
                        #we now have a list of the form [pivot, stuff counterclockwise pivot, stuff clockwise pivot]
                        #swap pivot into the middle of the list forming [stuff <= pivot, pivot, stuff>pivot]
                        plist[start] = plist[i-1]
                        plist[i-1] = pivot_item
                        temp = permuted_list[i-1]
                        permuted_list[i-1] = permuted_list[0]
                        permuted_list[0]=temp
                        #recursively sort the two sublists
                        if (i-2)-start > 0:
                            working_stack.append((start,i-2))
                        if end - i > 0:
                            working_stack.append((i,end))
            # having dropped through the while loop, we now have plist sorted in clockwise order 
            # relative to p0->q with points pi s.t. p0->pi is colinear with p0->q are at the head of the list
            
        return permuted_list


    def opposite(self,p0,p1):
        # returns a point which is in the opposite direction from p1 relative to p0
        return location(p0.x1-p1.subtract(p0).x1,p0.x2-p1.subtract(p0).x2)

    def perpendicular(self,p):
        # returns a point which is perpendicular to the point p (relative to (0,0))
        return location(-1*p.x2, p.x1)

    def direction(self,p1,p2,p3):
        ### returns direction between p1->p2 and p1->p3, is positive if direction is clockwise ###
        return self.cross_product(p3.subtract(p1),p2.subtract(p1))

    def cross_product(self,p1,p2):
        #takes two locations and returns their cross product
        global type_world
        if type_world == 'cartesian':
            return p1.x1*p2.x2 - p2.x1*p1.x2
        else:
            raise typeError
    
    def heading_to_radianangle(self,heading):
        # where radian angle of 0 points east
        temp = ((90-heading)/180.0)*math.pi
        return temp
    
    def radianangle_to_heading(self,angle):
        # where radian angle of 0 points east
        temp = 90-(180*angle/math.pi)
        return temp
    
    def new_location(self,heading,distance):
        #returns a location which is distance away from the origional location in direction heading
        # assumes objects have locations
        global type_world
        temp_theta = self.heading_to_radianangle(heading)
        if type_world == 'cartesian':
            temp_x1 = self.location.x1 + (math.cos(temp_theta)*distance)
            temp_x2 = self.location.x2 + (math.sin(temp_theta)*distance)
        else:
            raise typeError
        return location(temp_x1,temp_x2)

    def distance_between(self,p1,p2):
        ## returns distance between two points
        global type_world
        if type_world == 'cartesian':
            return math.sqrt((p1.x1-p2.x1)**2+(p1.x2-p2.x2)**2)
        else:
            raise typeError

    def along_line(self,line,distance):
        ## returns of a point along line distance between the ends of line where 0<=distance<=1 will be between points
        global type_world
        if type_world == 'cartesian':
            temp_x1 = line.p1.x1 + (line.p2.x1 - line.p1.x1)*distance
            temp_x2 = line.p1.x2 + (line.p2.x2 - line.p1.x2)*distance
        else:
            raise typeError
        return location(temp_x1,temp_x2)

    def midpoint(self,p1,p2):
        #returns midpoint between p1 and p2
        return self.along_line(line(p1,p2),0.5)

    def heading(self,tline):
        global type_world
        if type_world == 'cartesian':
            temp_theta = math.atan2((tline.p2.x2-tline.p1.x2),(tline.p2.x1-tline.p1.x1))
            temp_heading = self.radianangle_to_heading(temp_theta)
        else:
            raise typeError
        return temp_heading

    def rotate_line(self,tline,angle):
        #takes a line and returns a new line rotated by angle (positive in clockwise)
        global type_world
        if type_world == 'cartesian':
            temp_length = self.distance_between(tline.p1,tline.p2)
            theading = self.heading(tline)
            theading = theading + angle
            
            temp_theta = self.heading_to_radianangle(theading)
            delta_x = math.cos(temp_theta)*temp_length
            delta_y = math.sin(temp_theta)*temp_length
            temp_point = location(tline.p1.x1+delta_x,tline.p1.x2+delta_y)
            temp_line = line(tline.p1,temp_point)
        else:
            raise typeError
        return temp_line

    def translate_line(self,tline,p):
        # translates a line to make starting point coincide with point p
        global type_world
        if type_world == 'cartesian':
            delta_x = tline.p2.x1 - tline.p1.x1
            delta_y = tline.p2.x2 - tline.p1.x2
            end_point = location(p.x1+delta_x,p.x2+delta_y)
            return line(p,end_point)
        else:
            raise typeError
    
    def is_parallel(self,other):
        # determines if two lines are parallel
        global type_world
        if type_world == 'cartesian':
            if (self.p2.x1 == self.p1.x1)and (other.p2.x1 == other.p1.x1): #lines are both vertical
                return True
            elif self.p2.x1 == self.p1.x1 : # self is vertical and other is not
                return False
            elif other.p2.x1 == other.p1.x1: # other is vertical but self is not
                return False
            else:
                temp=((self.p2.x2-self.p1.x2)/(self.p2.x1-self.p1.x1))==\
                      ((other.p2.x2-other.p1.x2)/(other.p2.x1-other.p1.x1))
                return temp
        else:
            raise typeError

    def intersection(self,other):
        # returns the location of intersection of two lines
        global type_world
        if type_world == 'cartesian':
            if self.is_parallel(other):
                raise isParallel
            elif self.p1.x1 == self.p2.x1: #self is a vertical line
                mother = (other.p2.x2-other.p1.x2)/(other.p2.x1-other.p1.x1)
                bother = other.p1.x2 - (mother*other.p1.x1)
                x = self.p1.x1
                y = (mother*x) + bother
                temp = location(x,y)
                return temp
            elif other.p1.x1 == other.p2.x1: #other is a vertical line
                mself = (self.p2.x2-self.p1.x2)/(self.p2.x1-self.p1.x1)
                bself = self.p1.x2 - (mself*self.p1.x1)
                x = other.p1.x1
                y = (mself*x) + bself
                temp = location(x,y)
                return temp
            else:
                mself = (self.p2.x2-self.p1.x2)/(self.p2.x1-self.p1.x1)
                bself = self.p1.x2 - (mself*self.p1.x1)
                mother = (other.p2.x2-other.p1.x2)/(other.p2.x1-other.p1.x1)
                bother = other.p1.x2 - (mother*other.p1.x1)
                x=(bself-bother)/(mother-mself)
                y=(mself*x)+bself
                temp = location(x,y)
                return temp
                
        else:
            raise typeError

class location(world):

    def __init__(self,x,y):
        self.x1 = float(x)
        self.x2 = float(y)

    def __str__(self):
        return '(' + repr(self.x1) + ',' + repr(self.x2) + ')'

    def __eq__(self,other):
        return (self.x1 == other.x1) and (self.x2 == other.x2)

    def __ne__(self,other):
        return not((self.x1 == other.x1) and (self.x2 == other.x2))

    def add(self,other):
        return location(self.x1+other.x1,self.x2+other.x2)

    def subtract(self,other):
        return location(self.x1-other.x1,self.x2-other.x2)

class line(world):
    def __init__(self,p1,p2): # a line has two points, a start and end
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return '(' + self.p1.__str__() + ',' + self.p2.__str__() + ')'

    def draw_line(self):
        plot([self.p1.x1,self.p2.x1],[self.p1.x2,self.p2.x2])
