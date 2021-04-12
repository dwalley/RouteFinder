# heaps module

import math

class dheaps():

    def __init__(self,d,n,heap_type='max',less_than=None,greater_than=None):
        ###create an object of type dheap with length n, with each parent having up to d children###
        self.heap_size = 0 # maximum index for which there is data
        self.max_children = d
        self.length = n #size of the list holding the data
        self.heap_array = [] # internal representation, all elements of heap_array must be comparable
        self.lt_function = less_than
        self.gt_function = greater_than
        self.heap_type = heap_type # or could 'min'
        for i in range(0,n):
            self.heap_array.append(0)
            
    def lt(self,a,b):
        if self.lt_function == None:
            if self.heap_type == 'max': # None is negative infinity
                    return a < b
            else: # heap type in min and None is positive infinity
                if a == None:
                    return False
                elif b == None:
                    return True
                else:
                    return a < b
        else:
            return self.lt_function(a,b)
            
    def gt(self,a,b):
        if self.gt_function == None:
            if self.heap_type == 'max': # None is negative infinity
                    return a > b
            else: # heap type in min and None is positive infinity
                if a == None:
                    return True
                elif b == None:
                    return False
                else:
                    return a > b
        else:
            return self.gt_function(a,b)

    def set_value(self,i,value):
        assert type(i) == type(1) or type(i) == type(None)
        if i == None:
            return None
        elif i >= 1 and i <= self.length: # we are setting a value in an existing part of the heap
            self.heap_array[i-1] = value
            if i > self.heap_size:
                self.heap_size = i
            return value
        else: # we need to extend the heap
            for j in range(self.length,i):
                self.heap_array.append(0)
            self.heap_array[i-1] = value
            self.heap_size = i
            self.length = i
            return value

    def value(self,i):
        assert type(i) == type(1) or type(i) == type(None)
        if i == None:
            return None
        elif i >= 1 and i <= self.heap_size:
            return self.heap_array[i-1]
        else:
            raise heapIndexError

    def parent_index(self,i):
        assert type(i) == type(1)
        assert i >= 1 and i <= self.heap_size
        if i >1:
            return (i+self.max_children-2)//self.max_children
        else:
            return None

    def ith_child_index(self,n,i):
        # return the index of the ith child of nth element
        assert type(i) == type(1)
        assert type(n) == type(1)
        assert i >= 1 and  i <= self.max_children and n >= 1
##        print 'getting',i,'child of',n,'element'
        if n*self.max_children - self.max_children + i + 1<= self.heap_size:
            return n*self.max_children - self.max_children + i + 1
        else:
            return None
        


    def heapify(self,k):
        # assumes the child dtrees of element k are valid heaps of type heap_type
        # but self.value(k) might not satisify the heap criteria
        if self.heap_type == 'max':
            extreme_index = k
            extreme_value = self.value(k)
            for j in range(1,self.max_children+1):
                temp_index = self.ith_child_index(k,j)
                if temp_index != None:
                    if self.lt(extreme_value,self.value(temp_index)): # we found a bigger element, keep track of it
                        extreme_value = self.value(temp_index)
                        extreme_index = temp_index
            if extreme_index == k: # we did not find any larger elements among the children
                return None
            else: # we did find a larger element, swap it up the tree and recurr pushing our initial element down
                self.set_value(extreme_index,self.value(k))
                self.set_value(k,extreme_value)
                self.heapify(extreme_index)
        elif self.heap_type == 'min':
            extreme_index = k
            extreme_value = self.value(k)
            for j in range(1,self.max_children+1):
                temp_index = self.ith_child_index(k,j)
                if temp_index != None:
                    if self.gt(extreme_value,self.value(temp_index)): # we found a smaller element, keep track of it
                        extreme_value = self.value(temp_index)
                        extreme_index = temp_index
            if extreme_index == k: # we did not find any larger elements among the children
                return None
            else: # we did find a smaller element, swap it up the tree and recurr pushing our initial element down
                self.set_value(extreme_index,self.value(k))
                self.set_value(k,extreme_value)
                self.heapify(extreme_index)
        else:
            raise heapTypeError


    def build_heap(self):
        for k in range(self.heap_size//self.max_children,0,-1):
            self.heapify(k)

    def heap_sort(self):
        self.build_heap()
        old_heap_size = self.heap_size
        for i in range(old_heap_size,1,-1):
            temp = self.value(i)
            self.set_value(i,self.value(1))
            self.set_value(1,temp)
            self.heap_size -= 1
            self.heapify(1)
        if self.heap_type == 'max':
            self.heap_type = 'min'
        elif self.heap_type == 'min':
            self.heap_type = 'max'
        else:
            raise heapTypeError
        self.heap_size = old_heap_size
        return self.heap_array

    def heap_maximum(self):
        if self.heap_type == 'max':
            return self.value(1)
        elif self.heap_type == 'min': # flip the heap to a max heap and return the first value
            self.heap_sort()
            return self.value(1)
        else:
            raise heapTypeError

    def heap_extract_max(self):
        if self.heap_size < 1:
            return None
        else:
            if self.heap_type == 'max':
                heap_max = self.value(1)
                self.set_value(1,self.value(self.heap_size))
                self.set_value(self.heap_size,heap_max)
                self.heap_size -= 1
                self.heapify(1)
                return heap_max
            elif self.heap_type == 'min':
                self.heap_sort()
                heap_max = self.value(1)
                self.set_value(1,self.value(self.heap_size))
                self.set_value(self.heap_size,heap_max)
                self.heap_size -= 1
                self.heapify(1)
                return heap_max
            else:
                raise heapTypeError
            
    def heap_change_key(self,i,key):
        if self.heap_type == 'max':
            gt_result = self.gt(self.value(i),key)
            if gt_result: # we are decreasing the key in a max heap
                self.set_value(i,key)
                self.heapify(i)
            else: # we are increasing the key in a max heap
                self.set_value(i,key)
                j = self.parent_index(i)
                while j != None and self.lt(self.value(j),self.value(i)): #bubble value up the heap as necessary
                    temp = self.value(j)
                    self.set_value(j,self.value(i))
                    self.set_value(i,temp)
                    i = j
                    j = self.parent_index(j)
        elif self.heap_type == 'min':
            if self.lt(self.value(i),key):
                self.set_value(i,key)
                self.heapify(i)
            else:
                self.set_value(i,key)
                j = self.parent_index(i)
                while j != None and self.gt(self.value(j),self.value(i)): #bubble value up the heap as necessary
                    temp = self.value(j)
                    self.set_value(j,self.value(i))
                    self.set_value(i,temp)
                    i = j
                    j = self.parent_index(j)
        else:
            raise heapTypeError

    def heap_insert(self,key):
        self.heap_size += 1
        self.set_value(self.heap_size,None)
        self.heap_change_key(self.heap_size,key)
        

