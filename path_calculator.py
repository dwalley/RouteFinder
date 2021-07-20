## path_calculator encapsulates algorithms for calculating optimum paths
## within a hexagon field.

import world
import hexagon
import hexcontrol
import numpy
import pylab

class path_calculator:

    def __init__(self,hexcontroler):
        self.start_hex_path_element = None
        # note paths always start at the center of the hex field
        self.hex_controler = hexcontroler
        # hexcontroler is assumed to have at least 2 levels in the hex tree
        self.paths_dictionary = {} # is a flat dictionary, unlike tree of hex dictionaries
        self.start_hex = hexcontroler.lowest_center_hex
        #convert costs to list of numpy arrays, benefits to numpy array
        # also initializes hexcontroler roots
        self.hex_controler.arrayize_costs_benefits()
        for root_hex in self.hex_controler.roots:
            for temp_key,temp_hex in root_hex.hexagon_dictionary.items():
                self.paths_dictionary[temp_key] = hex_path_element(temp_hex)
##        print 'start_location is', self.start_hex.location, 'with hexcontroller',hexcontroler
        # 6-tuple of lists of hex_pata_data objects where the ith list is the ith ripple from start_hex
        #    in that tuple element
        # adjacent elements of the ripple list are physically contiguous except where hex field boundaries come in
        self.ripple_sextant_lists = ([[]],[[]],[[]],[[]],[[]],[[]])
        self.sextant_look_back_stack = ([],[],[],[],[],[])
        self.num_ripples = [-1,-1,-1,-1,-1,-1]
        self.num_better_paths = 0
        # set up the first two ripples
        self.initialize_ripple_out()
        for temp_ripple in range(0,self.hex_controler.convex_hull_count+1):
            # ripple out by sextant
##            print 'RIPPLE NUMBER',temp_ripple
            for current_sextant in range(0,len(self.ripple_sextant_lists)):
                result = self.ripple_out(current_sextant)
##                print 'num ripples is',self.num_ripples
                if result:
                    self.step_forward(current_sextant)
            # cycle through the sextants until we have exhausted all look back improvements
            for current_sextant in range(0,len(self.ripple_sextant_lists)):
                self.initialize_look_back(current_sextant)
            current_sextant = 0
            while self.sextant_look_back_stack != ([],[],[],[],[],[]):
##                print 'size of look back stack is',len(self.sextant_look_back_stack[0]),
##                print len(self.sextant_look_back_stack[1]),len(self.sextant_look_back_stack[2]),
##                print len(self.sextant_look_back_stack[3]),len(self.sextant_look_back_stack[4]),
##                print len(self.sextant_look_back_stack[5])
                self.look_back(current_sextant)
                current_sextant = (current_sextant + 1)%6

    def initialize_look_back(self,current_sextant):
##        print 'look back stack for sextant',current_sextant,' ripple level',self.num_ripples[current_sextant]
        for current_hex_path_element in self.ripple_sextant_lists[current_sextant][self.num_ripples[current_sextant]]:
            self.sextant_look_back_stack[current_sextant].append(current_hex_path_element)
##            print "1 ",
##        print

    def look_back(self,current_sextant):
        # we start the look back with the outermost ripple, as we look back if we find a better path to
        # an element in another sextant, we hand it off to that sextant
##        print 'entered look back for sextant',current_sextant
        while self.sextant_look_back_stack[current_sextant] != []:
            temp_hex_path_element =   self.sextant_look_back_stack[current_sextant].pop()
            #look at adjacent hexs which are in the current or previous ripple to see if there is a better path
            for candidate_hexagon in temp_hex_path_element.hexagon.adjacent:
                candidate_hex_path_element = self.paths_dictionary[candidate_hexagon.key]
                if (candidate_hex_path_element.ripple_number <= temp_hex_path_element.ripple_number) and\
                    (candidate_hex_path_element.hexagon.key not in temp_hex_path_element.benefactor_dictionary) and\
                    (candidate_hex_path_element.hexagon != self.start_hex):
                    # we have a valid candidate.
                    # see if going sideways or backwards yields a better path
                    #  if so, the path to candidate hex will be updated
                    # we don't consider going back to some place where we picked up a benefit previously
                    found_better_path = self.local_optimize_path(candidate_hex_path_element,temp_hex_path_element)
                    if found_better_path:
                        self.num_better_paths +=1
##                        candidate_hex_path_element.draw_path()
##                        pylab.show()
##                        if self.num_better_paths > 10:
##                            raise iAmGettingTired
                        if candidate_hex_path_element.sextant != temp_hex_path_element.sextant:
                            self.sextant_look_back_stack[candidate_hex_path_element.sextant]\
                                                        .append(candidate_hex_path_element)
                        else:
                            self.sextant_look_back_stack[current_sextant].append(candidate_hex_path_element)
        return True

    def local_optimize_path(self,candidate_hex_path_element,temp_hex_path_element):
        for adjacent_index in range(0,6):
            if temp_hex_path_element.hexagon.adjacent[adjacent_index] == candidate_hex_path_element.hexagon:
                break
        else:
            raise lostOurWay
        temp = candidate_hex_path_element.costs_benefits_less_than(temp_hex_path_element.total_cost_benefit,\
                                                                   temp_hex_path_element.hexagon.costs[adjacent_index],\
                                                                   candidate_hex_path_element.hexagon.benefit)
        if temp != False:
            # it is better to go to candidate hex from temp hex than the previously found path to candidate hex
            self.update_best_path(candidate_hex_path_element, (adjacent_index - 3)%6)
            return True
        else:
            return False

    def initialize_ripple_out(self):
        #initialize the origin hex path element which is always at the center of the hex field
        self.start_hex_path_element = self.paths_dictionary[self.start_hex.key]
        # do some initialization
        self.start_hex_path_element.total_cost_benefit = 0.0
##        print 'in ripple_out initialization'
##        print 'start hex costs',self.start_hex_path_element.hexagon.costs
        temp_accrued_cost=[0.0 for temp in self.start_hex.costs[0]]
        self.start_hex_path_element.accrued_cost = numpy.array(temp_accrued_cost)
##        print 'start accrued costs is ',self.start_hex_path_element.accrued_cost
        temp_accrued_benefit = self.start_hex.benefit
        self.start_hex_path_element.accrued_benefit = numpy.array(temp_accrued_benefit)
##        print 'start accrued benefit is ',self.start_hex_path_element.accrued_benefit
        # put start hex in benefactor list to avoid coming back to the origin
        self.start_hex_path_element.benefactor_dictionary[self.start_hex.key]=self.start_hex_path_element
        self.start_hex_path_element.ripple_number = 0
        self.num_ripples = [0,0,0,0,0,0]
        return True
        

    def ripple_out(self,current_sextant):
        # returns True if there are new hex path data points to be added as we ripple out
        if self.num_ripples[current_sextant] >= self.hex_controler.convex_hull_count-1:
            return False
        if self.num_ripples[current_sextant] == 0:
            # we are making the first ripple, special case
            temp_hex_path_element = self.paths_dictionary[self.start_hex.adjacent[current_sextant].key]
            self.ripple_sextant_lists[current_sextant].append([temp_hex_path_element])
            temp_hex_path_element.predecessor = self.paths_dictionary[self.start_hex.key]
            temp_hex_path_element.ripple_number = 1
            temp_hex_path_element.sextant = current_sextant
            self.num_ripples[current_sextant] += 1
            return True
##            print 'accrued cost for sextant element',current_sextant,'is',temp_hex_path_element.accrued_cost
        # we have at least two ripple levels, we are not yet at the convex hull, and it gets a little more complicated
        current_ripple_level = self.num_ripples[current_sextant]
##        print 'current_ripple_level is',current_ripple_level
        next_ripple_level = current_ripple_level + 1
##        print 'next_ripple_level is',next_ripple_level
        current_ripple_length = len(self.ripple_sextant_lists[current_sextant][current_ripple_level])
##        print 'length of current ripple sextant is ',current_ripple_length
        # add an empty list for the next ripple
        self.ripple_sextant_lists[current_sextant].append([]) # add the next level list
        for i_current in range(0,current_ripple_length):
            # i_current indexes over the elements in the current ripple sextant list
            # candidates for the next ripple are all the hexs adjacent to a hex in the current sextant ripple
            temp_hex_path_element = self.ripple_sextant_lists[current_sextant][current_ripple_level][i_current]
            if i_current == 0: # we are looking at the first element of sextant
##            print 'first element of sextant'
##            print 'current sextant is',current_sextant,' element sextant is',temp_hex_path_element.sextant
                # add two hexs to the next ripple since these are the first hexs in a new sextant
                temp_hex_key = temp_hex_path_element.hexagon.adjacent[current_sextant].key
                self.ripple_sextant_lists[current_sextant][next_ripple_level].\
                                                    append(self.paths_dictionary[temp_hex_key])
                self.paths_dictionary[temp_hex_key].ripple_number = next_ripple_level
                self.paths_dictionary[temp_hex_key].sextant = temp_hex_path_element.sextant
            
                temp_hex_key = temp_hex_path_element.hexagon.adjacent[(current_sextant+1)%6].key
                self.ripple_sextant_lists[current_sextant][next_ripple_level].\
                                                    append(self.paths_dictionary[temp_hex_key])
                self.paths_dictionary[temp_hex_key].ripple_number = next_ripple_level
                self.paths_dictionary[temp_hex_key].sextant = temp_hex_path_element.sextant
            else: # we are adding ripple elements in a sextant list already started
##                print 'subsequent element of sextant'
##                print 'current sextant is',current_sextant,' element sextant is',temp_hex_path_element.sextant
                temp_hex_key = temp_hex_path_element.hexagon.adjacent[(current_sextant+1)%6].key
                self.ripple_sextant_lists[current_sextant][next_ripple_level].\
                                                    append(self.paths_dictionary[temp_hex_key])
                self.paths_dictionary[temp_hex_key].ripple_number = next_ripple_level
                self.paths_dictionary[temp_hex_key].sextant = temp_hex_path_element.sextant
##        print 'in ripple out'
##        print 'for sextant',current_sextant
##        print 'ripple sextant list is',self.ripple_sextant_lists[current_sextant]
        self.num_ripples[current_sextant] += 1
        return True
    #phew

    def step_forward(self,current_sextant):
        # calculate best step forward paths to the newly added elements
        # note that the first elements of each sextant is a special case where there is only
        #   one way to step out
        if self.num_ripples[current_sextant] >= 1: # cases for ripples 0 and 1 were previously handled as special cases
            not_first_element = False
            ripple_index = self.num_ripples[current_sextant]
            #print ('in step forward')
            #print ('current ripple sextant is',current_sextant)
            #print (self.ripple_sextant_lists[current_sextant][ripple_index])
            for temp_path_element in self.ripple_sextant_lists[current_sextant][ripple_index]:
                if not_first_element:
                    candidate_best_step_out_indices = [((temp_path_element.sextant-3)%6),\
                                                       ((temp_path_element.sextant-2)%6)]
                    best_predecessor_index = self.find_best_predecessor(temp_path_element,\
                                                                        candidate_best_step_out_indices)
                    self.update_best_path(temp_path_element,best_predecessor_index)
                else: #this is the first hex in a new sextant, only one way to get there from here
                    current_sextant = temp_path_element.sextant
                    self.update_best_path(temp_path_element,((temp_path_element.sextant-3)%6))
                    not_first_element = True
        else:
            raise rippleError

    def draw_ripple(self,ripple_level):
        if ripple_level >= len(self.ripple_sextant_lists[0]) or ripple_level < 0 or type(ripple_level) != type(1):
            print ('ripple level is',ripple_level)
            print ('type of ripple_level is',type(ripple_level))
            raise nonexistantRippleLevel
        for current_sextant in range(0,len(self.ripple_sextant_lists)):
            for temp_hex_path_element in self.ripple_sextant_lists[current_sextant][ripple_level]:
                temp_hex_path_element.hexagon.draw()
                if temp_hex_path_element.predecessor != None:
                    line_to_predecessor = world.line(temp_hex_path_element.hexagon.location,\
                                                     temp_hex_path_element.predecessor.hexagon.location)
                    line_to_predecessor.draw_line()
                
            

    def find_best_predecessor(self,path_element,adjacent_index_list):
        # returns index from adjacent_index_list which is best predecessor to current hex_path_element #
        # start with the first adjacent path element
        current_adjacent_index = adjacent_index_list[0]
        current_adjacent_hexagon = path_element.hexagon.adjacent[current_adjacent_index]
        current_path_element = self.paths_dictionary[current_adjacent_hexagon.key]
        # calculate total cost/benefit in going from temp adjacent to current path element
        # remember the cost is the cost of coming here from there but the benefit is from being here
        current_total_cost_benefit = \
                                path_element.compute_total_cost_benefit\
                                (current_path_element.total_cost_benefit,\
                                 current_adjacent_hexagon.costs[(current_adjacent_index + 3) % 6],\
                                 path_element.hexagon.benefit)
        for temp_adjacent_index in adjacent_index_list[1:]:
            temp_adjacent_hexagon = path_element.hexagon.adjacent[temp_adjacent_index]
            temp_path_element = self.paths_dictionary[temp_adjacent_hexagon.key]
            # calculate total cost/benefit in going from temp adjacent to current path element
            # remember the cost is the cost of coming here from there but the benefit is from being here
            temp_total_cost_benefit = \
                                    path_element.compute_total_cost_benefit\
                                    (temp_path_element.total_cost_benefit,\
                                     temp_adjacent_hexagon.costs[(current_adjacent_index + 3) % 6],\
                                     path_element.hexagon.benefit)
            if temp_total_cost_benefit < current_total_cost_benefit:
                current_adjacent_index = temp_adjacent_index
                current_total_cost_benefit = temp_total_cost_benefit
        # having dropped through the for loop, current_adjacent_index now points to the best adjacent
        return current_adjacent_index

    def update_best_path(self,path_element,adjacent_index):
         #updates path to path_element hex formed by going from adjacent hex to path_element hex
        #print ('in update best path')
        #print ('path element ripple number is',path_element.ripple_number)
        #print ('path element sextant is',path_element.sextant)
        #print ('adjacent index is',adjacent_index)
        adjacent_hexagon = path_element.hexagon.adjacent[adjacent_index]
        adjacent_path_element = self.paths_dictionary[adjacent_hexagon.key]
        path_element.predecessor = adjacent_path_element
        path_element.accrued_cost = adjacent_path_element.accrued_cost +\
                                    adjacent_path_element.hexagon.costs[((adjacent_index + 3) % 6)]
        #print ('path element accrued cost is',path_element.accrued_cost)
        path_element.accrued_benefit = adjacent_path_element.accrued_benefit + path_element.hexagon.benefit
        #print ('in update_best_path')
        #print ('adjacent path element hexagon costs ',adjacent_path_element.hexagon.costs)
        path_element.total_cost_benefit = path_element.compute_total_cost_benefit\
                                          (adjacent_path_element.total_cost_benefit,\
                                           adjacent_path_element.hexagon.costs[(adjacent_index + 3) % 6],
                                           path_element.hexagon.benefit)
        path_element.benefactor_dictionary = adjacent_path_element.benefactor_dictionary
        if True in [temp_benefit > 0 for temp_benefit in path_element.hexagon.benefit]:
            path_element.benefactor_dictionary[path_element.hexagon.key]=path_element
        
class hex_path_element:

    def __init__(self,hexagon):
        self.hexagon = hexagon
        self.accrued_cost = numpy.array([]) # total optimal accrued cost getting to this hexagon
        self.accrued_benefit = numpy.array([]) #total optimal accrued benefit in getting to this hexagon
        self.benefactor_dictionary = {} # dictionary of benefactors contributing to accrued benefit
        self.total_cost_benefit = None # increasingly positive means increased cost
        self.predecessor = None # predecessor in chain of hexagons which accounts for costs and benefits
        self.ripple_number = -1
        # sextants are analogous to quadrants in a square world
        self.sextant = -1 # sextant in 0 .. 5 giving orientation relative to original hexagon, uses sorted adjacents

    def draw_path(self):
        temp_hex_path_element = self
        while temp_hex_path_element.predecessor != None:
            temp_hex_path_element.hexagon.draw()
            line_to_predecessor = world.line(temp_hex_path_element.hexagon.location,\
                                             temp_hex_path_element.predecessor.hexagon.location)
            line_to_predecessor.draw_line()
            temp_hex_path_element = temp_hex_path_element.predecessor
        temp_hex_path_element.hexagon.draw() #draw the origin hexagon

    def costs_benefits_less_than(self,other_total_cost_benefit,costs,benefits):
        # returns value of cost_benefit with costs factored in if it is less than self.total_cost_benefit #
        # encapsulates comparison of costs.  Note can not include benefits in optimization.  
        # They are just accounted for.
        for cost in costs:
            other_total_cost_benefit += cost
        if (self.total_cost_benefit == None):
            return False
        if other_total_cost_benefit < self.total_cost_benefit:
            return other_total_cost_benefit
        else:
            return False

    def compute_total_cost_benefit(self,combined_cost_benefit,costs,benefits):
        # returns single number resulting from adding costs and subtracting benefits to combined_cost_benefit #
        # higher number means more cost and less benefit
##        print 'in compute_total_cost_benefit'
##        print 'initial combined cost_benefit ',combined_cost_benefit
##        print 'costs ',costs
##        print 'benefit',benefits
        if combined_cost_benefit == None:
            temp_cost_benefit = 0.0
        else:
            temp_cost_benefit = combined_cost_benefit
        for cost in costs:
            temp_cost = float(cost)
            temp_cost_benefit += temp_cost
        for benefit in benefits:
            temp_benefit = float(benefit)
            temp_cost_benefit -= temp_benefit
        return temp_cost_benefit

    def add_costs(self,costs_1, costs_2):
        # returns numpy array which is the sum of the numpy arrays costs_1 and costs_2 which must be same length #
        return costs_1+costs_2

    def add_benefits(self,benefits_1,benefits_2):
        # returns numpy array sum of the numpy arrays benefits_1 and benefits_2 which must be same length, or null #
        if len(benefits_1) == 0:
            return benefits_2
        elif len(benefits_2) == 0:
            return benefits_1
        else:
            return benefits_1 + benefits_2

                
