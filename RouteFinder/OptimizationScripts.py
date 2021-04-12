# Optimization algorithms

import Lecture3

from Lecture3 import sqrt,fib,fib1,isPalindrome,factorize,mergeSort,mergeIsElementOf


def test_kv():
    
    cost_list = [1,2,3,4,7,3,8,9,3,6,3,7,8,4,5,6,7,5,2,6,1,7,9,2,7,3,4,8,5,9,1,2,3,4,5,6,7,8,9]
    value_list =[2,2,3,1,3,5,7,4,8,5,6,4,4,8,5,9,1,3,4,5,6,2,7,8,3,9,3,6,4,7,9,8,7,6,5,4,3,2,1]
    max_cost = 30
    return solveKnapsack(cost_list,value_list,max_cost)


def solveKnapsack(cost_list,value_list,max_cost):
    ### takes list of costs and list of values, returns max value with total cost <= max cost
    assert type(cost_list) == type([])
    assert type(value_list) == type([])
    assert len(cost_list) == len(value_list)
    assert type(max_cost) == type(1) 
    index = len(cost_list)-1
    results_dict={}
    result = knapsack_maxvalue(cost_list,value_list,index,max_cost,results_dict)
    return result

def knapsack_maxvalue(cost_list,value_list,index,max_cost,results_dict):
    ### returns maximum value subject to cost constraint ###
    if (index,max_cost) in results_dict:
        return results_dict[(index,max_cost)]
    else:
        if index < 0: # no more items to consider
            results_dict[(index,max_cost)]=0
            return 0
        elif max_cost == 0: # can't add any more items
            results_dict[(index,max_cost)]=value_list[index]
            return 0
        else:
            if cost_list[index] > max_cost: # too expensive to take item
                temp = knapsack_maxvalue(cost_list,value_list,index-1,max_cost,results_dict)
                results_dict[(index,max_cost)]=temp
                return temp
            else: #look at values from taking and not taking item
                temp1 = knapsack_maxvalue(cost_list,value_list,index-1,max_cost,results_dict)
                temp2 = value_list[index]+ \
                        knapsack_maxvalue(cost_list,value_list,index-1,(max_cost-cost_list[index]),results_dict)
                results_dict[(index,max_cost)]=max(temp1,temp2)
                return max(temp1,temp2)



items_values = {'watch':9,'radio':7,'vase':8,'painting':20}
# is a dictionary with 2-tuples of an items as a string and its dollar value

items_costs = {'watch':5,'radio':3,'vase':2,'painting':8}
# is a dictionary with 2-tuples of an item as a string and its cost

items_count = {'watch':3,'radio':3,'vase':3,'painting':3}
#items_count = {'watch':2,'radio':2,'vase':2,'painting':2}
# is a dictionary with 2-tuples of an item and the number of such items available.

knapsack_capacity = 5
# cost that a knapsack can carry

knapsack_contents = []
# list of items in the knapsack

S1=set([1,2,3,4,5])

def test_mkt():
    global items_counts,items_costs,items_values
##    test_list = ['watch','radio','vase']
    test_list = available_items_list(items_count)
    print test_list
    for i in test_list:
        print i, items_costs[i],items_values[i]
    return make_knapsack_tree(test_list,knapsack_capacity,items_costs,items_values)

def make_knapsack_tree(list,max_cost,cost_dictionary,value_dictionary):
    ### builds a recursive tree list of [(index,cost,value) tuples, subtree from not taking element,###
    ###subtree from taking element] ###
    assert type(list) == type([])
    assert type(max_cost) == type(1) or type(max_cost) == type(1.0)
    assert max_cost >= 0
    assert type(cost_dictionary) == type({})
    assert type(value_dictionary) == type({})
    result = []
    if (list == []) or (max_cost == 0):
        return result
    else:
        # initialiaze the root node
        node = len(list)-1,max_cost,0
        dont_include_subtree = make_dont_include_subtree(node,list,cost_dictionary,value_dictionary)
        do_include_subtree = make_do_include_subtree(node,list,cost_dictionary,value_dictionary)
        result = [node,dont_include_subtree,do_include_subtree]
        return result
    return None

def make_dont_include_subtree(node,list,cost_dictionary,value_dictionary):
    ### makes left (don't include) subtree
##    print 'make_dont called with node and list ',node, list
    if node[0] <= 0: # we are in our base case
        return [(node[0]-1,node[1],node[2]),[],[]]
    else: # we have one or more elements in our list which we are not going to include
        new_list_index = node[0]-1 #decrement our list counter
        new_cost = node[1] #unchanged since we did not include the nodal item
        new_value = node[2]
        new_subnode = new_list_index,new_cost,new_value
        if new_cost > 0:
            new_dont_include_subtree = make_dont_include_subtree(new_subnode,list,cost_dictionary,value_dictionary)
            new_do_include_subtree = make_do_include_subtree(new_subnode,list,cost_dictionary,value_dictionary)
        else: # new_cost equals 0 and we can't go further down the recursion due to no available resources
            new_dont_include_subtree = []
            new_do_include_subtree = []
        result = [new_subnode,new_dont_include_subtree,new_do_include_subtree]
##        print 'make_dont returns ',result
        return result

def make_do_include_subtree(node,list,cost_dictionary,value_dictionary):
    ### makes right (do include) subtree
##    print 'make_do called with node and list ',node, list
    new_cost = node[1]-cost_dictionary[list[node[0]]] # subtract cost of including item from available cost
    if new_cost < 0: #item is too expensive, terminate this branch of recursion
        return []
    if node[0] <= 0: # we are in our base case
        new_list_index = node[0] - 1 #decrement our list counter
        new_value = node[2]+value_dictionary[list[node[0]]]
        new_subnode = new_list_index,new_cost,new_value
        return [new_subnode,[],[]]
    else: # we have one or more elements in our list which we are going to include
        new_list_index = node[0] - 1 #decrement our list counter
        new_value = node[2]+value_dictionary[list[node[0]]]
        new_subnode = new_list_index,new_cost,new_value
        if new_cost > 0:
            new_dont_include_subtree = make_dont_include_subtree(new_subnode,list,cost_dictionary,value_dictionary)
            new_do_include_subtree = make_do_include_subtree(new_subnode,list,cost_dictionary,value_dictionary)
        else: # new_cost equals 0 and we can't go further down the recursion due to no available resources
            new_dont_include_subtree = []
            new_do_include_subtree = []
        result = [new_subnode,new_dont_include_subtree,new_do_include_subtree]
##        print 'make_do returns ',result
        return result

def knapsack_value(contents,value_dictionary):
    ### returns the sum of the values of the contents ###
    assert type(contents) == type([])
    if contents == []:
        return 0
    total_value = 0
    for item in contents:
        try:
            temp_value = value_dictionary[item]
            if type(temp_value) != (type(1) or type(1.0)):
                print 'Bad value dictionary entry: ',item, temp_value
                return None
            else:
                total_value = total_value + temp_value
        except KeyError:
            print item,' is not in the value dictionary'
            return None

    return total_value

def knapsack_cost(contents,cost_dictionary):
    ### returns the sum of the costs of the contents ###
    total_cost = 0
    for item in contents:
        try:
            temp_value = cost_dictionary[item]
            if type(temp_value) != (type(1) or type(1.0)):
                print 'Bad cost dictionary entry: ',item, temp_value
                return None
            else:
                total_cost = total_cost + temp_value
        except KeyError:
            print item,' is not in the cost dictionary'
            return None

    return total_cost

def sort_defined_values(items,value_dictionary):
    ### takes a list items which are keys in the key:value dictionary and sorts them by value lowest to highest"""
    ### does some checking and calls sort_defined_values_primitive which does the work
    try:
        try:
            assert type(items) == type([])
            try:
                assert type(value_dictionary) == type({})
                return sort_defined_values_primitive(items,value_dictionary)
            except AssertionError:
                print 'value_dictionary is not a dictionary'
        except AssertionError:
            print 'items is not a list'
            return None
    except KeyError:
        print 'Some item in items is not in value_dictionary'

def sort_defined_values_primitive(items,value_dictionary):

    if len(items) < 2:
        return items
    else:
        result = []
        temp_items1 = sort_defined_values_primitive(items[0:(len(items)/2)],value_dictionary)
        temp_items2 = sort_defined_values_primitive(items[(len(items)/2):],value_dictionary)
        i,j = 0,0
        while (i < len(temp_items1)) and (j < len(temp_items2)):
            if value_dictionary[temp_items1[i]] <  value_dictionary[temp_items2[j]]:
                result.append(temp_items1[i])
                i +=1
            else:
                result.append(temp_items2[j])
                j +=1
        if i == len(temp_items1):
            result.extend(temp_items2[j:])
        else:
            result.extend(temp_items1[i:])
        return result

def available_items_list(items_count):
    ### takes a dictionary of item, count pairs and returns a list with count duplications of item in list###
    result = []
    for i in items_count:
        for j in range(0,items_count[i]):
            result.append(i)
    return result


def greedyKnapsackFill(knapsack_capacity,items_count,items_costs,items_values):
    ### returns a list with cost not exceeding capacity with items collected via greedy algorithm ###
    # items_count is a dictionary with value[key] being the number of items of type key available
    # items_costs is a dictionary with value[key] being the cost of including one item of type key
    # item_values is a dictionary with value[key] being the value of including one item of type key
    result = []
    temp_items_list = []
    items_list = available_items_list(items_count)
##    print 'items_list is ',items_list
    sorted_items_list = sort_defined_values(items_list,items_values)
##    print 'sorted_items_list is ',sorted_items_list
    temp_knapsack_cost = 0
    while (temp_knapsack_cost <= knapsack_capacity) and (sorted_items_list != []):
        temp_item = sorted_items_list.pop()
##        print 'temp_item is ',temp_item
        temp_knapsack_cost += items_costs[temp_item]
##        print 'temp_knapsack_cost is ',temp_knapsack_cost
        if temp_knapsack_cost <= knapsack_capacity:
##            print 'adding ',temp_item
            result.append(temp_item)
##            print 'current result is ',result
    return result

def add_unique(item,list):
    ### adds list with item item added to list if not already present
    assert type(list) == type([])
    temp_list = list[:]
    if len(list) == 0:
        return [item]
    else:
        present = False
        for i in list:
            if i == item:
                return temp_list
        temp_list.append(item)
        return temp_list
                

def all_subsets(a_set):
    ### takes a set of items and returns a list consisting of all subsets of the initial set ###
    try:
        assert type(a_set) == type(set([]))
        if len(a_set) == 0:
            return [set()]
        temp_set = a_set.copy()
        temp_set2 = a_set.copy()
        result = [a_set]
        element_list = []
        while (len(temp_set) >= 1):
            element_list = element_list + [temp_set.pop()]
        for i in range(0,len(a_set)):
            temp_list = all_subsets(a_set - set([element_list[i]]))
##            print 'i is ',i
            for j in temp_list:
##                print 'j is ',j
                result = add_unique(j,result)
##            result = result + all_subsets(a_set - set([element_list[i]])) 
##            print result
##        print element_list
        return result
    except AssertionError:
        print 'all_sublists requires a list for its argument'

def all_sublists(a_list):
    ### takes a list of items and returns a list consisting of all sublists of the initial list ###
    try:
        assert type(a_list) == type([])
        if len(a_list) == 0:
            return [[]]
        temp_list = a_list[:]
        temp_list2 = a_list[:]
        result = [a_list]
        element_list = []
        while (len(temp_list) >= 1):
            element_list = element_list + [temp_list.pop()]
        for i in range(0,len(a_list)):
            temp_list = all_sublists(a_list[:i]+a_list[(i+1):])
##            print 'i is ',i
            for j in temp_list:
##                print 'j is ',j
                result = add_unique(j,result)
##            print result
##        print element_list
        return result
    except AssertionError:
        print 'all_sublists requires a list for its argument'

def exhaustiveKnapsackFill(knapsack_capacity,items_count,items_costs,items_values):
    ### solves Knapsack problem by enumeration  ###
    # items_count is a dictionary with value[key] being the number of items of type key available
    # items_costs is a dictionary with value[key] being the cost of including one item of type key
    # item_values is a dictionary with value[key] being the value of including one item of type key
    result = []
    best_value = 0
    items_list = available_items_list(items_count)
    all_possible_combinations = all_sublists(items_list)
    for i in all_possible_combinations:
        if (knapsack_value(i,items_values) > best_value) and (knapsack_cost(i,items_costs) <= knapsack_capacity):
            result = i
    return result
