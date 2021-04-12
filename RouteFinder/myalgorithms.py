# Algorithms module

#import numpy
import random
import math

class myalgorithms:

    def random_select(self,select_list,k):
        ### returns the kth element (counting starts at 0)###
        ###of a sorted version of select_list without sorting select_list, will rearrange it tho###

        def internal_random_select(select_list,k,p,q):# assumes k is between p and q inclusive
            if p == q:
                return select_list[k]
            #select a random pivot between p and q inclusive
            pivot_index = random.randrange(p,q)
            temp_element = select_list[p]
            select_list[p]= select_list[pivot_index]
            pivot = select_list[pivot_index]
            select_list[pivot_index]=temp_element
            #do a quicksort type partition of select_list between p and q, returning i where i points to pivot location
            i = p+1
            for j in range(p+1,q+1):
                if select_list[j] > pivot:
                    pass
                else: #it is <= pivot, move it to the left and increment pointer
                    temp_element = select_list[j]
                    select_list[j]= select_list[i]
                    select_list[i]= temp_element
                    i += 1
            # we now have gone through the list moving all elements <= pivot, i points to start of elements > pivot
            # restore the pivot
            pivot_index = i-1
            temp_element = select_list[pivot_index]
            select_list[pivot_index]= pivot
            select_list[p]= temp_element
            # if i-1 == k return select_list[i], otherwise recur on the left or right depending on k<i-1 or k>i-1
            if pivot_index == k:
                return select_list[pivot_index]
            elif k < pivot_index: # recur on left sublist
                return internal_random_select(select_list,k,p,pivot_index-1)
            else: # k is > pivot_index
                return internal_random_select(select_list,k,pivot_index+1,q)
                

        assert type(select_list) == type([])
        assert type(k)== type(1) and k <= len(select_list)
        if len(select_list) == 1:
            return select_list[0]
        else:
            element = internal_random_select(select_list,k,0,len(select_list)-1)
        return element
        

    def radix_sort(self,sort_list,max_value):
        ###takes a list of nonnegative integers less than max_value and returns a sorted list using a naive radix sort###

        def ith_digit(temp_number,base,i):
            assert type(temp_number) == type(1)
            assert type(base) == type(1)
            assert type(i) == type(1) and i >= 1
            temp_leading_digits = (temp_number // int(math.pow(base,i))) *  int(math.pow(base,i))
            if i == 1:
                return temp_number - temp_leading_digits
            else:
                temp_trailing_digits = int(math.fmod(temp_number,int(math.pow(base,i-1))))
                temp_result = temp_number - temp_leading_digits - temp_trailing_digits
                temp_result = temp_result // int(math.pow(base,i-1))
            return temp_result

        def base_count_sort(temp_list,base,digit_location):
            assert type(base) == type(1)
            assert type(digit_location) == type(1) and digit_location >= 1
            bin_list = []
            for i in range(0,base):
                bin_list.append(0)
            for element in temp_list:
                bin_list[ith_digit(element,base,digit_location)] +=1
            for i in range(1,base):
                bin_list[i] = bin_list[i] + bin_list[i-1]
            output_list = []
            for i in range(0,len(sort_list)):
                output_list.append(0)
            for i in range(len(temp_list)-1,-1,-1):
                element = temp_list[i]
                digit = ith_digit(element,base,digit_location)
                output_list[bin_list[digit]-1]=element
                bin_list[digit] += -1
            return output_list
                
        assert type(sort_list)==type([])
        assert type(max_value) == type(1) and max_value >=1
        list_len = len(sort_list)
        if list_len <= 1:
            return sort_list
        else:
            k = int(math.log(list_len,2))
            base = int(math.pow(2,k))
            num_digits = int(math.log(max_value,base))+1
            temp_list = sort_list
            for digit_location in range(1,num_digits+1):
                temp_list = base_count_sort(temp_list,base,digit_location)
            return temp_list

    def count_sort(self,sort_list,low_n,high_n,order='ascending'):
        ### returns sorted list (destroying list)where all elements are integers between low_n and high_n inclusive ###
        assert type(sort_list) == type([])
        assert type(low_n) == type(1)
        assert type(high_n) == type(1)
        k = high_n - low_n +1
        # make a list with an appropriate number of bins and initialize to zero
        bin_list = []
        for i in range(0,k):
            bin_list.append(0)
        for element in sort_list:
            bin_list[element-low_n] +=1
        for i in range(1,k):
            bin_list[i] = bin_list[i] + bin_list[i-1]
        # make output list and initialize
        output_list = []
        for i in range(0,len(sort_list)):
            output_list.append(0)
        #place elements in output list
        for i in range(len(sort_list)-1,-1,-1):
            element = sort_list[i]
            output_list[bin_list[element-low_n]-1]=element
            bin_list[element-low_n] += -1
        return output_list
        

    def quick_sort(self,temp_list,order= 'ascending'):
        #takes a list of comparable elements and sorts it in place
        assert type(temp_list) == type([])
        start = 0
        end = len(temp_list)-1
        working_stack = [(start,end)]
        max_working_stack = 1
        while len(working_stack) != 0:
            start,end = working_stack.pop()
            #handle some trivial cases
            if temp_list == []:  #handle empty lists
                return None
            elif start >= end: #at most one element list, no sorting to do
                pass
            elif end-start == 1:# we have a 2 element list
                if temp_list[start] <= temp_list[end]:
                    pass
                else:
                    temp = temp_list[end]
                    temp_list[end]=temp_list[start]
                    temp_list[start]=temp
            else:# we have at least a 3 element list to work on
                #pick a random pivot
                pivot_index = random.randrange(start,end)
                #switch the pivot with the head of the list
                pivot = temp_list[pivot_index]
                temp_list[pivot_index]=temp_list[start]
                temp_list[start]=pivot
                #go through list making two sublists, the first consisting of all elements <= pivot,
                # the second consisting of elements greater than pivot
                i=start + 1 # points to the start of the list greater than pivot
                j=start + 1 # index over the length of the list
                while j <= end:
                    if temp_list[j] > pivot:
                        j +=1
                    else:# it is <= pivot, swap it into the left side and increment 
                        temp = temp_list[j]
                        temp_list[j] = temp_list[i]
                        temp_list[i]=temp
                        i+=1
                        j+=1
                #we now have a list of the form [pivot, stuff <= pivot, stuff > pivot]
                #swap pivot into the middle of the list forming [stuff <= pivot, pivot, stuff>pivot]
                temp_list[start] = temp_list[i-1]
                temp_list[i-1] = pivot
                #recursively sort the two sublists
                if (i-2)-start > 0:
                    working_stack.append((start,i-2))
                if end - i > 0:
                    working_stack.append((i,end))
        return None

    def fib(self,n):
        # returns nth Fibonacci number
        assert type(n) == type(1)
        if n>45:# too big a number for numpy to handle on a 32 bit machine
            raise integeroverflowinfibcalltonumpy
        elif n == 1:
            return 1
        else:
            m = numpy.mat([[1,1],[1,0]])
            return self.power(m,n-1)[0,0]

    def power(self,item,n):
        #takes an item which can be multiplied and raises it to the nth power
        assert type(n)==type(1)
        assert n>0
        if n == 1:
            return item
        elif (n//2)*2 == n: # n is even
            return self.power(item,n//2)**2
        else: # n is odd
            return (self.power(item,(n-1)//2)**2)*item

    def insert_sort(self,temp_list,order='ascending'):
        # take a list of comparable items and return the sorted the list
        # good for smaller lists O(n squared)
        assert type(temp_list) == type([])
        list_length = len(temp_list)
    
        if list_length <=1: #list is already sorted
            return temp_list
        if order == 'descending':
            for j  in range(1,list_length): #iterate over the 2nd through last element in list
                k = j-1
                while (k >= 0) and (temp_list[j] > temp_list[k]):
                    k = k-1
                if k == -1: #temp_list[j] is bigger than any of its predecessors
                    temp_list = [temp_list[j]] + temp_list[:j] + temp_list[j+1:]
                elif k == j-1: # temp_list[j] is smaller than all of its predecessors, go to next iteration
                    pass
                else:
                    temp_list = temp_list[:k+1] + [temp_list[j]] + temp_list[k+1:j] + temp_list[j+1:]
        else: # sort in ascending order
            for j  in range(1,list_length): #iterate over the 2nd through last element in list
                k = j-1
                while (k >= 0) and (temp_list[j] < temp_list[k]):
                    k = k-1
                if k == -1: #temp_list[j] is smaller than any of its predecessors
                    temp_list = [temp_list[j]] + temp_list[:j] + temp_list[j+1:]
                elif k == j-1: # temp_list[j] is bigger than all of its predecessors, go to next iteration
                    pass
                else:
                    temp_list = temp_list[:k+1] + [temp_list[j]] + temp_list[k+1:j] + temp_list[j+1:]
        return temp_list

    def merge_sort(self,sort_list,order='ascending'):
        # take a list of comparable items and return the sorted list
        # good for bigger lists O(n log n)
        assert type(sort_list) == type([])
        list_length = len(sort_list)
        if list_length == 1:
            return sort_list
        else:
            breakpoint = list_length//2
            first_list = self.merge_sort(sort_list[0:breakpoint],order)
            second_list = self.merge_sort(sort_list[breakpoint:],order)
            i = 0 # index into first list
            j = 0 # index into second list
            temp_list = []
            if order == 'descending':
                while (i <= len(first_list)-1) and (j <= len(second_list)-1): # both indices are pointing short of the end
                    if first_list[i] > second_list[j]:
                        temp_list.append(first_list[i])
                        i += 1
                    else:
                        temp_list.append(second_list[j])
                        j += 1
                # either i or j is now pointing past the end of the list
                if i > len(first_list)-1: # we are done adding from first list, append remaining elements from second list
                    temp_list.extend(second_list[j:])
                else: # j maxed out, done adding from second list, append remainging elements from first list
                    temp_list.extend(first_list[i:])
            else: #sort in ascending order
                while (i <= len(first_list)-1) and (j <= len(second_list)-1): # both indices are pointing short of the end
                    if first_list[i] < second_list[j]:
                        temp_list.append(first_list[i])
                        i += 1
                    else:
                        temp_list.append(second_list[j])
                        j += 1
                # either i or j is now pointing past the end of the list
                if i > len(first_list)-1: # we are done adding from first list, append remaining elements from second list
                    temp_list.extend(second_list[j:])
                else: # j maxed out, done adding from second list, append remainging elements from first list
                    temp_list.extend(first_list[i:])
        return temp_list


    def binary_search(self,element,search_list,order = 'ascending'):
        # takes an element and a sorted list, all of which are comparable.
        # returns integer index of element in list, None if element is not in list
        assert type(search_list) == type([])
        i = 0
        k = len(search_list)-1
        while i <= k:
            j = i + (k-i)//2 # pick an index half way between i and k
            if order == 'descending': #list is descending
                if search_list[j] == element:
                    return j
                elif search_list[j] < element: # element will be found in left side of list
                    k = j-1
                else: # element will be found in right side of list
                    i = j+1
            else: # list is ascending
                if search_list[j] == element:
                    return j
                elif search_list[j] > element: # element will be found in left side of list
                    k = j-1
                else: # element will be found in right side of list
                    i = j+1
        return None


# heaps class

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
        


class binary_search_tree():
    ### class for manipulating binary search trees where the tree property is that left is < and right is >= ###

    def __init__(self,key):
        self.key = key
        self.left_sub_tree = None
        self.right_sub_tree = None
        self.parent = None

    def tree_delete(self,t,z):
        ### delete node z from tree t ###
        if z.left_sub_tree == None:
##            print 'deleting node with no left sub tree'
            self.tree_transplant(t,z,z.right_sub_tree)
        elif z.right_sub_tree == None:
##            print 'deleting node with no right sub tree'
            self.tree_transplant(t,z,z.left_sub_tree)
        else:
##            print 'deleting node with both left and right sub trees'
            y = self.tree_minimum(z.right_sub_tree)
##            print 'right subtree minimum of',z.key,'has key',y.key
##            print 'the parent key of said node is',y.parent.key
            if y.parent != z:
                self.tree_transplant(t,y,y.right_sub_tree)
                y.right_sub_tree = z.right_sub_tree
                y.right_sub_tree.parent = y
            self.tree_transplant(t,z,y)
            y.left_sub_tree = z.left_sub_tree
            y.left_sub_tree.parent = y

    def tree_transplant(self,t,u,v):
        ### replaces one subtree u with another subtree v within tree t ###
        if u.parent == None: # u is the root node of the tree, i.e. t and u both point to the same node
##            print 't.key is',t.key,'u.key is',u.key
            u.key = v.key
        elif u == u.parent.left_sub_tree:
            u.parent.left_sub_tree = v
        else:
            u.parent.right_sub_tree = v
        if v != None:
            v.parent = u.parent

    def tree_insert(self,t,z):
        ### insert z into a binary tree with root node t ###
        y = None
        x = t
        while x != None:
            y = x
            if z.key < x.key:
                x = x.left_sub_tree
            else:
                x = x.right_sub_tree
        z.parent = y
        if z.key < y.key:
            y.left_sub_tree = z
        else:
            y.right_sub_tree = z
        return None
    
    def inorder_tree_walk(self,node):
        if node != None:
            self.inorder_tree_walk(node.left_sub_tree)
            print (node.key)
            self.inorder_tree_walk(node.right_sub_tree)

    def preorder_tree_walk(self,node):
        if node != None:
            print (node.key)
            self.preorder_tree_walk(node.left_sub_tree)
            self.preorder_tree_walk(node.right_sub_tree)

    def postorder_tree_walk(self,node):
        if node != None:
            self.postorder_tree_walk(node.left_sub_tree)
            self.postorder_tree_walk(node.right_sub_tree)
            print (node.key)

    def tree_search(self,start_node,key):
        x = start_node
        while x != None and x.key != key:
            if key < x.key:
                x = x.left_sub_tree
            else:
                x = x.right_sub_tree
        return x
    
    def tree_minimum(self,start_node):
        x = start_node
        while x.left_sub_tree != None:
            x = x.left_sub_tree
        return x

    def tree_maximum(self,start_node):
        x = start_node
        while x.right_sub_tree != None:
            x = x.right_sub_tree
        return x

    def tree_succesor(self,node):
        if node.right_sub_tree != None:
            return self.tree_minimum(node.right_sub_tree)
        y = node.parent
        while y != None and node == y.right_sub_tree:
            node = y
            y = y.parent
        return y

    def tree_predecessor(self,node):
        if node.left_sub_tree != None:
            return self.tree_maximum(node.left_sub_tree)
        y = node.parent
        while y != None and node == y.left_sub_tree:
            node = y
            y = y.parent
        return y
