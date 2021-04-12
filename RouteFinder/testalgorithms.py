# test algorithms

##from myalgorithms import *
import myalgorithms
from myalgorithms import dheaps
from myalgorithms import binary_search_tree
#import numpy


#from pylab import *
import time

import random

doer = myalgorithms.myalgorithms()

n = 100
temp_list = []
for i in range(0,n):
    temp_list.append(int(random.random()*1000))

# test binary search trees

temp_keys = [12,5,18,2,9,15,19,17]
test_node = binary_search_tree(23)
print ('test node key is',test_node.key)
node_list = []
for i in range(0,len(temp_keys)):
##    print 'i is',i,'temp_keys[i] is',temp_keys[i]
    node_list.append(binary_search_tree(temp_keys[i]))
    if i > 0:
        node_list[0].tree_insert(node_list[0],node_list[i])
print ('done making node list')
root_node = node_list[0]

print ('root node key is',root_node.key)
print ('left sub node key is',root_node.left_sub_tree.key)
print ('right sub node key is',root_node.right_sub_tree.key)

print ('calling inorder tree walk')
root_node.inorder_tree_walk(root_node)

print ('calling preorder tree walk')
root_node.preorder_tree_walk(root_node)

print ('calling postorder tree walk')
root_node.postorder_tree_walk(root_node)

print ('calling tree delete of node with key',node_list[5].key)
root_node.tree_delete(root_node,node_list[5])

print ('calling inorder tree walk')
root_node.inorder_tree_walk(root_node)


##print 'starting insertion sort'
####print temp_list
##output_list = doer.insert_sort(temp_list,'descending')
####print output_list
##output_list = doer.insert_sort(temp_list,'ascending')
####print output_list
##
##print 'finished insertion sort'
##
##print 'starting merge sort'
####print temp_list
####output_list2 = doer.merge_sort(temp_list,'descending')
######print output_list
##output_list1 = doer.merge_sort(temp_list,'ascending')
####print output_list
##print 'finished merge sort'
##
##print 'starting binary search'
##element = 2
##i = doer.binary_search(element,output_list1,'ascending')
##print 'index of element is ',i
##i = doer.binary_search(element,output_list2,'descending')
##print 'index of element is ',i
##
##n = 20
##item = numpy.mat([[1,1],[1,0]])
##result = doer.power(item,n)
##print item,'to the ',n,'power is ',result
##
##for n in range(1,47):
##    result = doer.fib(n)
##    print 'the',n,'Fibonacci number is',result
##

##temp_list = [3,1,5,4,2,7,6]

##for m in range(0,1):
####    temp_list = [3,1,5,4,2,7,6]
##    temp_list = []
##    
##for i in range(0,n):
##    temp_list.append(random.choice(range(1,1000)))
##print temp_list
##print 'starting quick sort'    
##print 'lenth of list is',len(temp_list)
##doer.quick_sort(temp_list,'ascending')
##print temp_list
##print 'finished quick sort'
##print

##print 'starting count sort'
####print 'temp_list is ',temp_list
##output_list = doer.count_sort(temp_list,1,9)
####print 'output_list is',output_list
##print 'finished with cout sort'
##print 'first 100 elements of output list is',output_list[0:100]



##print 'starting radix sort'
####print 'temp_list is ',temp_list
##output_list = doer.radix_sort(temp_list,1000)
####print 'output_list is',output_list
##print 'finished with radix sort'
##print 'first 100 elements of output list is',output_list[0:100]

##for i in range(0,n):
##    temp_list = []
##    for j in range(0,n):
##        temp_list.append(int(random.random()*1000))
####    print 'temp_list is',temp_list
####    print 'random select for position',i,'is'
##    print doer.random_select(temp_list,i),
####    print 'resultant temp_list is',temp_list

# test dheaps

##test_heap = dheaps(2,3,'max')
##
##test_heap.heap_array = [16,4,10,14,7,9,3,2,8,1]
##test_heap.heap_size = 10
##test_heap.length = 10
##
##print 'printing values'
##for i in range(1,test_heap.heap_size+1):
##    print test_heap.value(i),
##
##print
##
##for i in range(1,test_heap.heap_size+1):
##    print i,test_heap.value(i),'has parent',test_heap.parent_index(i),test_heap.value(test_heap.parent_index(i))
##    for j in range(1,test_heap.max_children+1):
##        print i,test_heap.value(i),'has child',test_heap.ith_child_index(i,j),\
##              test_heap.value(test_heap.ith_child_index(i,j))
##
##test_heap.heapify(2)
##print 'after heapifying at element 2'
##for i in range(1,test_heap.heap_size+1):
##    print i, test_heap.value(i),
##
##print
##
##test_heap.set_value(1,4)
##test_heap.set_value(2,1)
##test_heap.set_value(3,3)
##test_heap.set_value(4,2)
##test_heap.set_value(5,16)
##test_heap.set_value(6,9)
##test_heap.set_value(7,10)
##test_heap.set_value(8,14)
##test_heap.set_value(9,8)
##test_heap.set_value(10,7)
##
##print 'heap size is',test_heap.heap_size
##print 'heap length is',test_heap.length
##
##print 'printing values of second list'
##for i in range(1,test_heap.heap_size+1):
##    print test_heap.value(i),
##
##print
##
##test_heap.build_heap()
##print 'after building heap'
##for i in range(1,test_heap.heap_size+1):
##    print i, test_heap.value(i),
##print
##
##print 'building 7heap and populating in reverse order'
##test_heap = dheaps(7,3,'max')
##for i in range(1,test_heap.length+1):
##    test_heap.set_value(i,i)
##
##print 'printing values of 7heap list'
##for i in range(1,test_heap.heap_size+1):
##    print test_heap.value(i),
##
##print
##
##test_heap.build_heap()
##print 'after building 7heap'
##for i in range(1,test_heap.heap_size+1):
##    print i, test_heap.parent_index(i),test_heap.value(i)
##print
##
##print 'building dheap and populating with random numbers'
##test_heap = dheaps(2,8,'max')
##for i in range(1,test_heap.length+1):
##    test_heap.set_value(i,random.choice([0,1,2,3,4,5,6,7,8,9]))
##print 'commencing heap sort values of dheap list'
####for i in range(1,test_heap.heap_size+1):
####    print test_heap.value(i),
####print
##test_heap.heap_sort()
##print 'finished with heap sort'
##print 'first 100 sorted numbers is',test_heap.heap_array[:min(100,test_heap.length-1)]

##test_heap = dheaps(3,3,'max')
##
##test_heap.heap_array = [16,14,10,8,7,9,3,2,4,1]
##test_heap.heap_size = 10
##test_heap.length = 10
##
##print 'printing values'
##for i in range(1,test_heap.heap_size+1):
##    print test_heap.value(i),
##
##print
##
##test_heap.heap_change_key(9,15)
##
##print 'heap size is',test_heap.heap_size
##print 'printing values after heap change key of 9th item from 4 to 15'
##for i in range(1,test_heap.heap_size+1):
##    print test_heap.value(i),
##print
##
##temp_max = test_heap.heap_maximum()
##print 'maximum is',test_heap.heap_maximum()
##
##print 'extracting maximum',test_heap.heap_extract_max()
##
##print 'residual heap is:'
##for i in range(1,test_heap.heap_size+1):
##    print test_heap.value(i),
##print
##
##print 'putting max back into the heap'
##test_heap.heap_insert(temp_max)
##print 'residual heap is:'
##for i in range(1,test_heap.heap_size+1):
##    print test_heap.value(i),
##print

##time.clock()
##times = []
##for j in range(2,20):
##    print 'building dheap and populating with random numbers'
##    test_heap = dheaps(j,10000,'max')
##    for i in range(1,test_heap.length+1):
##        test_heap.set_value(i,random.choice([0,1,2,3,4,5,6,7,8,9]))
##    print 'commencing heap sort values of dheap list'
##    ##for i in range(1,test_heap.heap_size+1):
##    ##    print test_heap.value(i),
##    ##print
##    start_time = time.clock()
##    test_heap.heap_sort()
##    finish_time = time.clock()
##    times.append(finish_time-start_time)
##    print 'finished with heap sort',j
##plot(times)
##show()
