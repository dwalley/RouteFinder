# test dheaps

from pylab import *
import time
from dheaps import *
import random

print random.random()
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
time.clock()
times = []
for j in range(2,20):
    print 'building dheap and populating with random numbers'
    test_heap = dheaps(j,10000,'max')
    for i in range(1,test_heap.length+1):
        test_heap.set_value(i,random.choice([0,1,2,3,4,5,6,7,8,9]))
    print 'commencing heap sort values of dheap list'
    ##for i in range(1,test_heap.heap_size+1):
    ##    print test_heap.value(i),
    ##print
    start_time = time.clock()
    test_heap.heap_sort()
    finish_time = time.clock()
    times.append(finish_time-start_time)
    print 'finished with heap sort',j
plot(times)
show()
