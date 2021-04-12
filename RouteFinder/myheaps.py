# heaps module

import math

class dheaps:

    __init__(self,d,n,heap_type='max'):
        #create an object of type dheap with depth n, with each parent having up to d children
        self.heap_size = int((math.pow(d,n)-1.0)/(d-1.0))
        self.max_children = d
        self.length = n
        self.heap_array = [] # internal representation, all elements of heap_array must be comparable
        self.heap_type = heap_type # or could 'min'
        for i in range(0,int((math.pow(d,n)-1.0)/(d-1.0))):
            self.heap_array.append(0)

    value(self,i):
        assert type(i) == type(1)
        assert i >= 1 and i <= self.heap_size
        return self.heap_array[i-1]

    parent_index(self,i):
        assert type(i) == type(1)
        assert i >= 1 and i <= self.heap_size
        return (i+self.max_children-2)//self.max_children

    ith_child_index(self,n,i):
        # return the index of the ith child of nth element
        assert type(i) == type(1)
        assert type(n) == type(1)
        assert i >= 1 and  i <= self.num_children and n >= 1
        if n*self.max_children - self.max_children + i + 1<= self.heap_size:
            return n*self.max_children - self.max_children + i + 1
        else:
            raise indexBeyondHeap


    heapify(self,k):
        # assumes the child dtrees of element k are valid heaps of type heap_type
        # but self.value(k) might not satisify the heap criteria
        if self.heap_type == 'max':
            extreme_index = k
            extreme_value = self.value(k)
            for j in range(1,self.max_children+1):
                try:
                    temp_index = self.ith_child_index(k,i)
                    if extreme_value < self.value(temp_index): # we found a bigger element, keep track of it
                        extreme_value = self.value(temp_index)
                        extreme_index = temp_index
                except indexBeyondHeap:
                    break
            if extreme_index == k: # we did not find any larger elements among the children
                return None
            else: # we did find a larger element, swap it up the tree and recurr pushing our initial element down
                self.heap_array[extreme_index]=self.heap_array[k]
                self.heap_array[k] = extreme_value
                self.heapify(extreme_index)
        elif self.heap_type == 'min':
            extreme_index = k
            extreme_value = self.value(k)
            for j in range(1,self.max_children+1):
                try:
                    temp_index = self.ith_child_index(k,i)
                    if extreme_value > self.value(temp_index): # we found a smaller element, keep track of it
                        extreme_value = self.value(temp_index)
                        extreme_index = temp_index
                except indexBeyondHeap:
                    break
            if extreme_index == k: # we did not find any larger elements among the children
                return None
            else: # we did find a smaller element, swap it up the tree and recurr pushing our initial element down
                self.heap_array[extreme_index]=self.heap_array[k]
                self.heap_array[k] = extreme_value
                self.heapify(extreme_index)
        else:
            raise heapTypeError
                

    
        

