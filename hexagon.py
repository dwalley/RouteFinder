# hexagon module

# encapsulates working with hexagons

from world import *

from pylab import *

import math


   
class hexagon(world):

    def __init__(self,x,y,od,angle,my_world):

        self.location = location(x,y) #defined in world
        self.outside_diameter = float(od)
        self.orientation = float(angle % 360) # heading 0 is north or up, 90 is east or right, etc.
        self.parents = [] # list of parent hexagons
        self.children = [] #list of children hexagons
        self.adjacent = [] #list of adjacent hexagons
        self.costs = [] # list of cost lists of going from self to adjacent hexagons
        self.benefit = [] # lists of benefits from arriving at self
        self.hexagon_dictionary = {}
        self.key = (0,)
        self.hexagon_dictionary[self.key]= self
        self.type = None
        # global_hexagon_dictionary is a dictionary whose key is a 4 tuple consisting of the two coordinates,
        # outside diameter, and angle.  The associated value is a pointer to that hexagon.

    def line_intersects(self,segment):
        ### returns true if line segment intersects hexagon, may overlap edge ###
        vertex_list = self.vertices()
        edge_list = []
        for i in range(0,6):
            edge_list.append(line(vertex_list[i],vertex_list[(i+1)%6]))
        for edge in edge_list:
            if self.segments_intersect(edge.p1,edge.p2,segment.p1,segment.p2):
                return True
        return False
        

    def is_interior(self,p):
        ### returns true if point p is interior to hexagon ###
        # note that the first three sides of the hexagon are included in the interior but not the last three #
        # this avoids the problem of a point being in more than one hexagon in a hexagon field #
        vertex_list = self.vertices()
##        print 'vertex_list is',vertex_list
        edge_list = []
        for i in range(0,6):
            edge_list.append(line(vertex_list[i],vertex_list[(i+1)%6]))
        for i in range(0,3): # see if p is on one of the first three edges
            if self.on_segment(edge_list[i].p1,edge_list[i].p2,p):
                return True
        for i in range(3,6): # see if p is on one of the last three edges
            if self.on_segment(edge_list[i].p1,edge_list[i].p2,p):
                return False
        x_max = max(v.x1 for v in vertex_list)
        q = location(x_max+1,p.x2)
        right_ray = line(p,q)
        num_intersections = 0
        for i in range(0,6):
            if self.proper_lines_intersect(right_ray,edge_list[i]): #see if ray intersects a side of hex
                num_intersections += 1
            if self.on_segment(right_ray.p1, right_ray.p2,vertex_list[i]):# see if ray intersects a vertex
                num_intersections += 1
        if num_intersections == 1:
            return True
        else:
            return False
            

    def make_subhexagons(self,n,my_world):
        # assumes self is part of a fully completed hex level with no duplicates and completed level dictionary
        #takes a hexagon and recurrsion level.  populates hexagon with n sublevels of subhexagons
        assert type(n) == type(1)
        assert n >= 0
        if n == 0:
            return None
        else: # make 1 or more levels of subtrees
            # levels will be madebreadth first
            # start my making the root hexagon for the next level
            current_root_hexagon = self.get_center()
            original_orientation = self.get_root().orientation
##            print 'origional orientation is',original_orientation
            
            temp_height = self.height()
##            print 'height is',temp_height
            
            sub_inside_diameter = self.distance_between(self.location,self.vertices()[0])/2
            sub_outside_diameter = self.calculate_outside_diameter(sub_inside_diameter)
            
            if original_orientation > 180:
                temp_orientation = original_orientation - ((1+pow(-1,temp_height))*45)
            else:
                temp_orientation = original_orientation - ((1+pow(-1,temp_height))*45)

##            print 'new orientation is',temp_orientation
                
            next_root_hexagon = hexagon(current_root_hexagon.location.x1, current_root_hexagon.location.x2,\
                                        sub_outside_diameter,temp_orientation,my_world)
            current_root_hexagon.children.append(next_root_hexagon)
            next_root_hexagon.parents.append(current_root_hexagon)
            next_root_hexagon.key = next_root_hexagon.make_key(my_world)
            next_root_hexagon.hexagon_dictionary = {}
            next_root_hexagon.hexagon_dictionary[next_root_hexagon.key]=next_root_hexagon

            # then iterate through all of the hexagons in the current level
            for self_hexagon_key in current_root_hexagon.hexagon_dictionary:
                self_hexagon = current_root_hexagon.hexagon_dictionary[self_hexagon_key]
##                print "self_hexagon key is",self_hexagon_key
            
                # make list of subhexagons starting with the center subhexagon
                subhexagon_locations=[self_hexagon.location]
                subhexagon_locations.extend(self_hexagon.vertices())

                if self_hexagon != current_root_hexagon:                            
                    #make the 7 subhexagons and append them to the children list
                    for i in range(0,7):
                        temp_hexagon = hexagon(subhexagon_locations[i].x1,subhexagon_locations[i].x2,\
                                                     sub_outside_diameter,temp_orientation,my_world)
                        temp_hexagon.parents=[self_hexagon]
                        self_hexagon.children.append(temp_hexagon)
                        #see if we need to update root dictionary, if not make temp_hexagon point to the existing hexagon
                        temp_hexagon1 = temp_hexagon.update_level_dictionary(my_world)
                        if temp_hexagon1 == temp_hexagon: #we did not find a duplicate in the level dictionary
                            pass
                        else: # found a duplicate.  fix children list to point to it.
##                            print 'we found a duplicate'
                            temp_hexagon = temp_hexagon1
                            self_hexagon.children.pop()
                            self_hexagon.append_unique(self_hexagon.children,temp_hexagon)
                        # temp_hexagon may now point to a hexagon created as subhexagon of a different parent hexagon
                        temp_hexagon.append_unique(temp_hexagon.parents,self_hexagon)
                else: # we are making the children of the level's root hexagon, having already made its center child
                    #make the 6 subhexagons and append them to the children list
                    for i in range(1,7):
                        temp_hexagon = hexagon(subhexagon_locations[i].x1,subhexagon_locations[i].x2,\
                                                     sub_outside_diameter,temp_orientation,my_world)
                        temp_hexagon.parents=[self_hexagon]
                        self_hexagon.children.append(temp_hexagon)
                        #see if we need to update root dictionary, if not make temp_hexagon point to the existing hexagon
                        temp_hexagon1 = temp_hexagon.update_level_dictionary(my_world)
                        if temp_hexagon1 == temp_hexagon: #we did not find a duplicate in the level dictionary
                            pass
                        else: # found a duplicate.  fix children list to point to it.
##                            print 'we found a duplicate'
                            temp_hexagon = temp_hexagon1
                            self_hexagon.children.pop()
                            self_hexagon.append_unique(self_hexagon.children,temp_hexagon)
                        # temp_hexagon may now point to a hexagon created as subhexagon of a different parent hexagon
                        temp_hexagon.append_unique(temp_hexagon.parents,self_hexagon)

##                print 'length of self_hexagon children list is',len(self_hexagon.children)

                # next code section assumes 0th element in children list is the center subhexagon
                # it also assumes that our list of hexagons does not contain duplicates.
                # this assumption is guaranteed by the call to update_root_dictionary which checks for duplicates
                
                # have each point to the next
                for i in range(1,6):
                    self_hexagon.children[i].append_unique(self_hexagon.children[i].adjacent,self_hexagon.children[i+1])
                self_hexagon.children[6].append_unique(self_hexagon.children[6].adjacent,self_hexagon.children[1])
                # have each point to the previous
                for i in range(1,6):
                    self_hexagon.children[i+1].append_unique(self_hexagon.children[i+1].adjacent,self_hexagon.children[i])
                self_hexagon.children[1].append_unique(self_hexagon.children[1].adjacent,self_hexagon.children[6])
                # have outer subhexs point to the center subhex
                for i in range(1,7):
                    self_hexagon.children[i].append_unique(self_hexagon.children[i].adjacent,self_hexagon.children[0])
                # have inner subhex point to the outer subhexs
                for i in range(1,7):
                    self_hexagon.children[0].append_unique(self_hexagon.children[0].adjacent,self_hexagon.children[i])

##                for i in range(0,7):
##                    print 'for child',i,'number of adjacent hexs is',len(self_hexagon.children[i].adjacent)

            # recurrsively make the next level
            if n-1 > 0:
                next_root_hexagon.make_subhexagons(n-1,my_world)


    def update_level_dictionary(self,my_world):
        #requires that self have a valid parents pointer
        new_key = self.make_key(my_world)
        root_hex = self.get_center()
        temp_hex = self
        new_x1 = self.location.x1
        new_x2 = self.location.x2
        new_r = self.outside_diameter
        for temp_parent in self.parents[0].adjacent:
            for temp_hex2 in temp_parent.children:
                temp_x1 = temp_hex2.location.x1
                temp_x2 = temp_hex2.location.x2
                if pow((temp_x1-new_x1),2) < pow((new_r / 6),2):
                    if pow((temp_x2-new_x2),2) < pow((new_r / 6),2):
                        # we are too close, return existing hex
                        return temp_hex2
        # if we made it through the for loop, no entry in the dictionary is too close
        # make a new entry in the level dictionary
        root_hex.hexagon_dictionary[new_key]=self
        return temp_hex

    def make_key(self,my_world):
        # makes a dictionary key for a hexagon
        # the key can be used to identify the hex's location in the tree
        key = self.parents[0].key+(len(self.parents[0].children)-1,)
        self.key = key
        return key
                                                                  

    def get_root(self):
        #returns a pointer to the root hexagon of which self is a part
        if self.parents == []:
            return self
        else:
            return self.parents[0].get_root()

    def get_center(self):
        # returns a pointer to the hexagon at the geometric center of the current level of the hex tree
        # note the geometric center is always the first hexagon made for that level
        temp_hex = self.get_root()
        current_level = self.height()
        for i in range(1,current_level+1):
            temp_hex = temp_hex.children[0]
        return temp_hex
            
    
    def inside_diameter(self):
        # intentionally complex to test components, does not make assumptions about geometry
        temp_vertices = self.vertices() # make list of the vertices of the hexagon
        temp_line = line(temp_vertices[0],temp_vertices[1]) # make line between 0th and 1st vertices
        temp_midpoint = self.midpoint(temp_line.p1,temp_line.p2) #find its midpoint
        temp_inside_diameter=self.distance_between(self.location,temp_midpoint) # find distance between center and midpoint
        return temp_inside_diameter

    def calculate_outside_diameter(self,given_inside_diameter):
        # a calculator which will return float of an outside diameter given an inside diameter of a hexagon
        if not(given_inside_diameter>0):
            raise invalidInsideDiameter
        else:
            temp_heading = self.orientation
            temp_heading = temp_heading + 30 #now points to center of a side of the hexagon
            if temp_heading > 360:
                temp_heading = temp_heading - 360
            mid_side = self.new_location(temp_heading,given_inside_diameter) #midpoint of the side of a hexagon
            center_to_midside_line = line(self.location,mid_side) # make line from center of hex to middle of side
            perpendicular = self.rotate_line(center_to_midside_line,90)
            side_line = self.translate_line(perpendicular,mid_side) # line starting at midpoint of side, following side
            towards_vertex = self.new_location(self.orientation,given_inside_diameter)
            line_towards_vertex = line(self.location,towards_vertex)
            vertex = line_towards_vertex.intersection(side_line)
            result = self.distance_between(vertex,self.location)
            return result
        

    def vertices(self):
        ### returns list of 6 locations of vertices of hexagon ###
        theta = self.orientation
        result = []
        for i in range(0,6):
            temp_location = self.new_location(self.orientation+i*60,self.outside_diameter)
            result.append(temp_location)
        return result

    def draw_line_to(self,other_hex):
        xlocs=[self.location.x1,other_hex.location.x1]
        ylocs=[self.location.x2,other_hex.location.x2]
        plot(xlocs,ylocs)
        return None

    def draw(self):
        
        xverts=[]
        yverts=[]
        temp = self.vertices()
        for i in temp:
            xverts.append(i.x1)
            yverts.append(i.x2)
        xverts.append(temp[0].x1)
        yverts.append(temp[0].x2)
        plot(xverts,yverts)
        return None

    def draw_neighborhood(self,num_adjacent):
        if num_adjacent < 1:
            self.draw()
        else:
            self.draw()
            for temp_hex in self.adjacent:
                temp_hex.draw_neighborhood(num_adjacent-1)

    def depth(self):
        # returns depth of a hexagon tree below self
        # assumes that self is part of a valid hex tree
        if self.children == []:
            i = 0
        else:
            temp_child = self.children[0]
            i = 1
            while temp_child.children !=  []:
                i += 1
                temp_child = temp_child.children[0]
        return i

    def height(self):
        # returns height of a hexagon tree above the given hexagon
        if self.parents == []:
            i = 0
        else:
            temp_parent = self.parents[0]
            i = 1
            while temp_parent.parents !=  []:
                i += 1
                temp_parent = temp_parent.parents[0]
        return i


    def draw_all_sublevels(self,n):
        #assumes self is a root hex, draws all sublevels up to and including n
        assert type(n) == type(1)
        assert n >= 0
        assert n<=self.depth()
        temp_root = self
        for i in range(0,n+1):
            for temp_key in temp_root.hexagon_dictionary:
                temp_hex = temp_root.hexagon_dictionary[temp_key]
                temp_hex.draw()
            if temp_hex.children != []:
                temp_root = temp_root.children[0]
        return None

    def draw_all_sublevels_connected_parents(self,n):
        #assumes self is a root hex, draws all sublevels up to and including n, and lines from hex to its parent
        assert type(n) == type(1)
        assert n >= 0
        assert n<=self.depth()
        temp_root = self
        for i in range(0,n+1):
            for temp_key in temp_root.hexagon_dictionary:
                temp_hex = temp_root.hexagon_dictionary[temp_key]
                temp_hex.draw()
                for temp_parent in temp_hex.parents:
                    temp_hex.draw_line_to(temp_parent)
            if temp_hex.children != []:
                temp_root = temp_root.children[0]
        return None
    
    def draw_all_sublevels_connected_adjacent(self,n):
        #assumes self is a root hex, draws all sublevels up to and including n, and lines from hex to its adjacents
        assert type(n) == type(1)
        assert n >= 0
        assert n<=self.depth()
        temp_root = self
        for i in range(0,n+1):
            for temp_key in temp_root.hexagon_dictionary:
                temp_hex = temp_root.hexagon_dictionary[temp_key]
                temp_hex.draw()
                for temp_adjacent in temp_hex.adjacent:
                    temp_hex.draw_line_to(temp_adjacent)
            if temp_hex.children != []:
                temp_root = temp_root.children[0]
        return None
    
    def draw_all_sublevels_connected_children(self,n):
        #assumes self is a root hex, draws all sublevels up to and including n, and lines from hex to its children
        assert type(n) == type(1)
        assert n >= 0
        assert n<=self.depth()
        temp_root = self
        for i in range(0,n+1):
            for temp_key in temp_root.hexagon_dictionary:
                temp_hex = temp_root.hexagon_dictionary[temp_key]
                temp_hex.draw()
                for temp_child in temp_hex.children:
                    temp_hex.draw_line_to(temp_child)
            if temp_hex.children != []:
                temp_root = temp_root.children[0]
        return None
        
    def draw_nth_sublevel(self,n):
        #assumes self is a root hex
        assert type(n) == type(1)
        assert n >= 0
        assert n<=self.depth()
        temp_root = self
        for i in range(0,n):
            temp_root = temp_root.children[0]
        for temp_key in temp_root.hexagon_dictionary:
            temp_hex = temp_root.hexagon_dictionary[temp_key]
            temp_hex.draw()
        return None

    def draw_nth_sublevel_connected_adjacent(self,n):
        #assumes self is a root hex, draws nth sublevel, and lines from hex to its adjacent hexs
        assert type(n) == type(1)
        assert n >= 0
        assert n<=self.depth()
        temp_root = self
        for i in range(0,n):
            temp_root = temp_root.children[0]
        for temp_key in temp_root.hexagon_dictionary:
            temp_hex = temp_root.hexagon_dictionary[temp_key]
            temp_hex.draw()
            for temp_adjacent in temp_hex.adjacent:
                temp_hex.draw_line_to(temp_adjacent)
        return None
    
    def draw_nth_adjacent_connections(self,n):
        #assumes self is a root hex, draws nth sublevel lines from hex to its adjacent hexs
        assert type(n) == type(1)
        assert n >= 0
        assert n<=self.depth()
        temp_root = self
        for i in range(0,n):
            temp_root = temp_root.children[0]
        for temp_key in temp_root.hexagon_dictionary:
            temp_hex = temp_root.hexagon_dictionary[temp_key]
            for temp_adjacent in temp_hex.adjacent:
                temp_hex.draw_line_to(temp_adjacent)
        return None
    
    def append_unique(self,hex_list,hex):
        #takes a list and appends hex if it is not already a part of the list
        if hex in hex_list:
            return None
        else:
            hex_list.append(hex)

    def sort_adjacent(self):
        ### sorts in place the adjacent hex list in temp_hex in clockwise order relative to temp_hex's heading ###
        p0 = self.location
        q = self.vertices()[0]
        plist = self.adjacent
        permuted_list = self.sort_segments(p0,q,plist) # world method
        # if there are costs associated with the adjacents, sort them too, if not do nothing
        if permuted_list != None and self.costs != []:
            temp_costs = range(0,len(permuted_list))
            for i in range(0,len(permuted_list)):
                    temp_costs[i] = self.costs[permuted_list[i]]
            self.costs = temp_costs
        self.adjacent = plist #this might be redundant
        return None

