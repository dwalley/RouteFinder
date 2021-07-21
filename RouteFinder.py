
# module for testing hexagon

from world import *
import hexcontrol
from hexagon import *
import myalgorithms
import cProfile

##import matplotlib.pyplot as plt
##from matplotlib.path import Path
##import matplotlib.patches as patches

from pylab import *

import path_calculator


# initialize world
my_world=world()
print('Type of world is ',my_world.type_world)

#test_hex = hexagon(0,0,1,90,my_world)
#print ('test_hex is ',test_hex)
#print ('location is ',test_hex.location.x1, test_hex.location.x2)
#print ('outside diameter is ',test_hex.outside_diameter)
#print ('the vertices of test_hex are located at ')
#for i in test_hex.vertices(): print ('        x=',i.x1,' y=',i.x2)

#p0 = location(0,0)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(-5,0)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(5,0)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(0,0.25)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(-5,0.25)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(1,0)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(0.5,0.866025403784)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(0,0.866025403784)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(0,0.866025403785)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(0,0.866025403783)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(-0.5,0.866025403784)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(-5,0.866025403784)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))
#p0 = location(5,0.866025403784)
#print ('x=',p0.x1,'y=',p0.x2,'is_interior to test_hex is',test_hex.is_interior(p0))

#p0 = hexagon(0,0,1,90,my_world)
#p1 = hexagon(1,0,1,0,my_world)
#p2 = hexagon(0,1,1,0,my_world)
#p3 = hexagon(-1,0,1,0,my_world)
#p4 = hexagon(0,-1,1,0,my_world)
#p5 = hexagon(1,1,1,0,my_world)
#p6 = hexagon(-1,1,1,0,my_world)
#p7 = hexagon(-1,-1,1,0,my_world)
#p8 = hexagon(1,-1,1,0,my_world)

#print (p2.location,' cross ',p3.location,' is',my_world.cross_product(p2.location,p3.location))
#print ('direction from ',p1.location,'->',p3.location,' to ',p1.location,'->',p2.location,' is ',\
#      my_world.direction(p1.location,p2.location,p3.location))
#print (p1.location,'->',p2.location,' intersects ',p3.location,'->',p4.location,'is',\
#      my_world.segments_intersect(p1.location,p2.location,p3.location,p4.location))

#p0.adjacent = [p1,p2,p3,p4,p5,p6,p7,p8]
###plist = [p1,p2,p3,p4]
###p0 = location(0,0)
###q = location(1,1)

#print ('starting sort_segments')
#p0.sort_adjacent()
#print ('relative to origin',p0.location,'with q equal',p0.vertices()[0],'the sorted plist is')
#for i in p0.adjacent:
#    print (i.location)



test_hex=hexagon(0,0,150,90,my_world)

#print ('test_hex is ',test_hex)
#print ('location is ',test_hex.location.x1, test_hex.location.x2)
#print ('outside diameter is ',test_hex.outside_diameter)
#temp = test_hex.orientation
#print ('radian angle is ',test_hex.heading_to_radianangle(temp))
#print ('outside diameter is',test_hex.outside_diameter,'; inside diameter is ',test_hex.inside_diameter())
#print (test_hex.calculate_outside_diameter(test_hex.inside_diameter()),\
#    ' is the recalcuated outside diameter based on the inside diameter')

#print ('the vertices of test_hex are located at ',)
#for i in test_hex.vertices(): print ('x=',i.x1,' y=',i.x2)

# n is the depth of the hexagon tree, must be at least 3
n=5

#print ('making subhexagons for',n,'level tree')

#cProfile.run('test_hex.make_subhexagons(n,my_world)')
test_hex.make_subhexagons(n,my_world)
#print ('finished making subhexagons')

#i=0
#for j in range(0,n+1):
#    i += 7**j
#print ('number of hexagons which would have been created recurrsively is ',i)

#temp_hex = test_hex
#temp_size = 0
#for j in range(0,n+1):
#    temp_size += len(temp_hex.hexagon_dictionary)
#    print ('size of',j,'level dictionary is ',len(temp_hex.hexagon_dictionary))
#    if temp_hex.children != []:
#        temp_hex = temp_hex.children[0]
#print ('total number of hexagons in the tree is ',temp_size)

test_hex_controler = hexcontrol.hexcontrol(test_hex,my_world)

#print ('starting to sort adjacent lists')
#cProfile.run('test_hex_controler.sort_adjacent_hexs()')
test_hex_controler.sort_adjacent_hexs()
#print ('finished sorting adjacent lists')

## test keyize'ing and unkeyize'ing pointers
#print ('keyizing pointers')
#test_hex_controler.keyize_pointers(my_world)
#print ('unkeyizing pointers')
#test_hex_controler.unkeyize_pointers()

## make sure pointers are correct for children by drawing hex tree
#figure()
#print ('drawing all sublevels ',min(7,n))
#print ('drawing all sublevels')
#test_hex.draw_all_sublevels(min(7,n))
#print(my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit)
#axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])

#figure()
#print ('drawing  nth sublevel ',min(7,n))
#test_hex.draw_nth_sublevel(min(7,n))
#print(my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit)
#axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])

#show()



print ('saving dictionary')
file_name = 'testout2.txt'

test_hex_controler.save_hex_tree(file_name,my_world)
print ('done saving dictionary')

file_name = 'testout2.txt'
print('reading dictionaries from',file_name)
# make a temporary root hex
root_hex = hexagon(0,0,0,0,my_world)
root_hex_controler = hexcontrol.hexcontrol(root_hex,my_world)
# load the stored dictionary into the root's dictionary, making hexs for each dictionary entry
test_hex = root_hex_controler.read_dictionary(file_name,my_world)
#print ('test_hex is ',test_hex)
#print ('location is ',test_hex.location.x1, test_hex.location.x2)
#print ('outside diameter is ',test_hex.outside_diameter)
temp = test_hex.orientation
#print ('radian angle is ',test_hex.heading_to_radianangle(temp))
#print ('outside diameter is',test_hex.outside_diameter,'; inside diameter is ',test_hex.inside_diameter())
#print (test_hex.calculate_outside_diameter(test_hex.inside_diameter()),' is the recalcuated outside diameter based on the inside diameter')

#print ('the vertices of test_hex are located at ',)
#for i in test_hex.vertices(): print ('x=',i.x1,' y=',i.x2)

print ('initializing hex controler')
test_hex_controler = hexcontrol.hexcontrol(test_hex,my_world)
n = test_hex.depth()
print ('depth of newly read in tree is',n)
print ('done reading dictionaries')

print('Generating random cost and benefits')
test_hex_controler.generate_random_costs()


print ('saving dictionary')
file_name = 'testout2.txt'

test_hex_controler.save_hex_tree(file_name,my_world)
print ('done saving dictionary')

print ('executing path calculator')
test_path = path_calculator.path_calculator(test_hex_controler)
print ('number of elements added to stack on look back is',test_path.num_better_paths)

figure()

print ('drawing ripples out from origin')
for ripple_level in range(0,test_path.num_ripples[0]):
#    if (ripple_level % 15) == 1:
#        test_path.draw_ripple(ripple_level)
    #print('ripple level is',ripple_level)
    test_path.draw_ripple(ripple_level)

print ('done rippling out from origin')
show()

##print ('translating field')
##test_hex_controler.translate_hex_field(location(500,0))
##print ('done translating field')
##
##print ('source_hex is ',test_hex_controler.source_hex)
##print ('location is ',test_hex_controler.source_hex.location.x1,\
##      test_hex_controler.source_hex.location.x2)
##print ('outside diameter is ',test_hex_controler.source_hex.outside_diameter)
##temp = test_hex_controler.source_hex.orientation
##print ('radian angle is ',test_hex.heading_to_radianangle(temp))
##print ('outside diameter is',test_hex_controler.source_hex.outside_diameter,\
##      '; inside diameter is ',test_hex_controler.source_hex.inside_diameter())
##print (test_hex_controler.source_hex.calculate_outside_diameter(test_hex.inside_diameter()),\
##      ' is the recalcuated outside diameter based on the inside diameter')
##
##print ('the vertices of test_hex are located at ',)
##for i in test_hex_controler.source_hex.vertices(): print ('x=',i.x1,' y=',i.x2)
##
##print ('executing path calculator')
##test_path = path_calculator.path_calculator(test_hex_controler)
##print ('number of elements added to stack on look back is',test_path.num_better_paths)
##
##print ('drawing ripples out from origin')
##figure()
##for ripple_level in range(0,test_path.num_ripples[0]):
####    if (ripple_level % 15) == 1:
####        test_path.draw_ripple(ripple_level)
##    test_path.draw_ripple(ripple_level)
##
##print ('done rippling out from origin')
##show()


##print ('rotating field')
##test_hex_controler.change_orientation(45)
##print ('done rotating field')
##
##print ('source_hex is ',test_hex_controler.source_hex)
##print ('location is ',test_hex_controler.source_hex.location.x1,\
##      test_hex_controler.source_hex.location.x2)
##print ('outside diameter is ',test_hex_controler.source_hex.outside_diameter)
##temp = test_hex_controler.source_hex.orientation
##print ('radian angle is ',test_hex.heading_to_radianangle(temp))
##print ('outside diameter is',test_hex_controler.source_hex.outside_diameter,\
##      '; inside diameter is ',test_hex_controler.source_hex.inside_diameter())
##print (test_hex_controler.source_hex.calculate_outside_diameter(test_hex.inside_diameter()),\
##      ' is the recalcuated outside diameter based on the inside diameter')
##
##print ('the vertices of test_hex are located at ',)
##for i in test_hex_controler.source_hex.vertices(): print ('x=',i.x1,' y=',i.x2)
##
##print ('executing path calculator')
##test_path = path_calculator.path_calculator(test_hex_controler)
##print ('number of elements added to stack on look back is',test_path.num_better_paths)
##
##print ('drawing ripples out from origin')
##figure()
##for ripple_level in range(0,test_path.num_ripples[0]):
####    if (ripple_level % 15) == 1:
####        test_path.draw_ripple(ripple_level)
##    test_path.draw_ripple(ripple_level)
##
##print ('done rippling out from origin')
##show()

##figure()
##
##print ('scaling field')
##test_hex_controler.change_scale(30)
##print ('done scaling field')
##
##print ('source_hex is ',test_hex_controler.source_hex)
##print ('location is ',test_hex_controler.source_hex.location.x1,\
##      test_hex_controler.source_hex.location.x2)
##print ('outside diameter is ',test_hex_controler.source_hex.outside_diameter)
##temp = test_hex_controler.source_hex.orientation
##print ('radian angle is ',test_hex.heading_to_radianangle(temp))
##print ('outside diameter is',test_hex_controler.source_hex.outside_diameter,\
##      '; inside diameter is ',test_hex_controler.source_hex.inside_diameter())
##print (test_hex_controler.source_hex.calculate_outside_diameter(test_hex.inside_diameter()),\
##      ' is the recalcuated outside diameter based on the inside diameter')
##
##print ('the vertices of test_hex are located at ',)
##for i in test_hex_controler.source_hex.vertices(): print ('x=',i.x1,' y=',i.x2)
##
##print ('executing path calculator')
##test_path = path_calculator.path_calculator(test_hex_controler)
##print ('number of elements added to stack on look back is',test_path.num_better_paths)
##print ('drawing ripples out from origin')
##for ripple_level in range(0,test_path.num_ripples[0]):
####    if (ripple_level % 15) == 1:
####        test_path.draw_ripple(ripple_level)
##    test_path.draw_ripple(ripple_level)
##
##print ('done rippling out from origin')
##show()

# draw the last few ripples

##print('drawing last few ripples')
### Uncomment next 5 lines only if the depth of the hex tree is at least 6
######figure()
######for i in range(15,20):
######    test_path.draw_ripple(ripple_level-1-i)
######axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
######show()
##figure()
##for i in range(10,15):
##    test_path.draw_ripple(ripple_level-1-i)
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##show()
##figure()
##for i in range(5,10):
##    test_path.draw_ripple(ripple_level-1-i)
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##show()
##figure()
##for i in range(0,5):
##    test_path.draw_ripple(ripple_level-1-i)
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##show()

print('drawing various lines')
figure()
p_start = location(0,0)
p_end = location(100,100)
previous_hex = None
for temp_hex in test_hex_controler.line_of_hexagons(p_start,p_end):
    temp_hex.draw()
    if previous_hex != None:
        temp_line = line(previous_hex.location,temp_hex.location)
        temp_line.draw_line()
    previous_hex = temp_hex
axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
title('Line of hexagons from'+str(p_start)+'to'+str(p_end))
show()

figure()
p_start = location(0,0)
p_end = location(0,500)
previous_hex = None
for temp_hex in test_hex_controler.line_of_hexagons(p_start,p_end):
    temp_hex.draw()
    if previous_hex != None:
        temp_line = line(previous_hex.location,temp_hex.location)
        temp_line.draw_line()
    previous_hex = temp_hex
axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
title('Line of hexagons from'+str(p_start)+'to'+str(p_end))
show()

figure()
p_start = location(0,0)
p_end = location(0,-500)
previous_hex = None
for temp_hex in test_hex_controler.line_of_hexagons(p_start,p_end):
    temp_hex.draw()
    if previous_hex != None:
        temp_line = line(previous_hex.location,temp_hex.location)
        temp_line.draw_line()
    previous_hex = temp_hex
axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
title('Line of hexagons from'+str(p_start)+'to'+str(p_end))
show()

figure()
p_start = location(0,0)
p_end = location(-200,-50)
previous_hex = None
for temp_hex in test_hex_controler.line_of_hexagons(p_start,p_end):
    temp_hex.draw()
    if previous_hex != None:
        temp_line = line(previous_hex.location,temp_hex.location)
        temp_line.draw_line()
    previous_hex = temp_hex
axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
title('Line of hexagons from'+str(p_start)+'to'+str(p_end))
show()

figure()
p_start = location(-200,-50)
p_end = location(-200,50)
previous_hex = None
for temp_hex in test_hex_controler.line_of_hexagons(p_start,p_end):
    temp_hex.draw()
    if previous_hex != None:
        temp_line = line(previous_hex.location,temp_hex.location)
        temp_line.draw_line()
    previous_hex = temp_hex
axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
title('Line of hexagons from'+str(p_start)+'to'+str(p_end))
show()

figure()

p_start = location(200,50)
p_end = location(-200,-50)
previous_hex = None
for temp_hex in test_hex_controler.line_of_hexagons(p_start,p_end):
    temp_hex.draw()
    if previous_hex != None:
        temp_line = line(previous_hex.location,temp_hex.location)
        temp_line.draw_line()
    previous_hex = temp_hex
axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
title('Line of hexagons from'+str(p_start)+'to'+str(p_end))
show()

####figure()

##test_location = location(0,0)
##print 'location is',test_location
##temp_containing_hex = test_hex_controler.lowest_hex_containing_point(test_location)
##print 'temp_containing_hex is ',temp_containing_hex
##print 'location is ',temp_containing_hex.location.x1, temp_containing_hex.location.x2
##print 'outside diameter is ',temp_containing_hex.outside_diameter
##
##test_location = location(10,10)
##print 'location is',test_location
##temp_containing_hex = test_hex_controler.lowest_hex_containing_point(test_location)
##print 'temp_containing_hex is ',temp_containing_hex
##print 'location is ',temp_containing_hex.location.x1, temp_containing_hex.location.x2
##print 'outside diameter is ',temp_containing_hex.outside_diameter
##
##test_location = location(50,50)
##print 'location is',test_location
##temp_containing_hex = test_hex_controler.lowest_hex_containing_point(test_location)
##print 'temp_containing_hex is ',temp_containing_hex
##print 'location is ',temp_containing_hex.location.x1, temp_containing_hex.location.x2
##print 'outside diameter is ',temp_containing_hex.outside_diameter
##
##test_location = location(50,-50)
##print 'location is',test_location
##temp_containing_hex = test_hex_controler.lowest_hex_containing_point(test_location)
##print 'temp_containing_hex is ',temp_containing_hex
##print 'location is ',temp_containing_hex.location.x1, temp_containing_hex.location.x2
##print 'outside diameter is ',temp_containing_hex.outside_diameter



##print 'generating random cost/benefit values for all levels of hex field'
##test_hex_controler.generate_random_costs()
##print 'done generating random cost/benefit values'
##
##file_name = 'testout11.txt'
##print 'saving dictionaries',file_name
##
##test_hex_controler.save_hex_tree(file_name,my_world)
##print 'done saving dictionaries'

##for draw_levels in range (0,min(6,n+1)):
##    figure()
##    print 'drawing all sublevels ',draw_levels
##    print 'drawing all sublevels'
##    test_hex.draw_all_sublevels(draw_levels)
##    axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##    title('all sublevels for level '+str(draw_levels))
##
##    figure()
##    print 'drawing  nth sublevel ',draw_levels
##    test_hex.draw_nth_sublevel(draw_levels)
##    axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##    title('all sublevel '+str(draw_levels))


##figure()
##print 'drawing all sublevels ',min(7,n)
##print 'drawing all sublevels'
##test_hex.draw_all_sublevels(min(7,n))
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##
##figure()
##print 'drawing  nth sublevel ',min(7,n)
##test_hex.draw_nth_sublevel(min(7,n))
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##

##figure()
##print 'drawing all sublevels with parent connections',min(7,n)
##print 'drawing all sublevels'
##test_hex.draw_all_sublevels_connected_parents(min(7,n))
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##title('all sublevels with parent connections')

##figure()
##print 'drawing all sublevels with adjacent connections',min(7,n)
##print 'drawing all sublevels'
##test_hex.draw_all_sublevels_connected_adjacent(min(7,n))
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##title('all sublevels with adjacent connections')

##figure()
##print 'drawing all sublevels with children connections',min(7,n)
##print 'drawing all sublevels'
##test_hex.draw_all_sublevels_connected_children(min(7,n))
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##title('all sublevels with children connections')

##figure()
##print 'drawing nth sublevel with adjacent connections',min(7,n)
##print 'drawing nth sublevel'
##test_hex.draw_nth_sublevel_connected_adjacent(min(7,n))
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##title('nth sublevel with adjacent connections')

##figure()
##print 'drawing nth sublevel connections without hexs',min(7,n)
##test_hex.draw_nth_adjacent_connections(min(7,n))
##axis([my_world.x1_lower_limit,my_world.x1_upper_limit,my_world.x2_lower_limit,my_world.x2_upper_limit])
##title('nth sublevel connections without hexs')




##doer = myalgorithms.myalgorithms()
##print 'generating difference list'
##difference_list = test_hex_controler.compare_centers()
##print 'doing merge sort'
##value_list = doer.merge_sort([i[2] for i in difference_list])
##print "first 100 entries in Sorted list of center differences is",\
##      [value_list[i] for i in range(0,min([len(value_list),100]))]

##print 'checking number of children'
##test_hex_controler.check_children()

show()



