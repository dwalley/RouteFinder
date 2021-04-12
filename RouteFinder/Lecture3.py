def sqrt(x):
    """ takes a positive number and returns the square root """
    x=float(x)
    if (x < 0):
        return None
    else:
        guess = 1
        tolerance = 0.000000001
        Iterations = 0
        MaxIterations = 100
        while ((((guess*guess)-x)**2) > (tolerance**2)) and (Iterations < MaxIterations) :
            guess = ((guess + (x/guess))/2)
            Iterations = Iterations + 1
##        print 'Iterations = ',Iterations
        return guess

def BarnYard():
    NumHeads = int(raw_input('Enter the number of heads: '))
    NumLegs = int(raw_input('Enter the number of legs: '))
    pigs , chickens = solve(NumHeads,NumLegs)
    if pigs == None:
        print 'There is an error'
    else:
        print 'The number of pigs is ',pigs
        print 'The number of chickens is ',chickens

def solve(NumHeads,NumLegs):
    NumHeads = int(NumHeads)
    NumLegs = int(NumLegs)
    for PossiblePigs in range(0,(NumHeads+1)):
        PossibleChickens = NumHeads - PossiblePigs
        if (((4*PossiblePigs)+(2*PossibleChickens)) == NumLegs):
            return PossiblePigs,PossibleChickens
    return (None,None)


def isPalindrome(s):
    """takes a string argument and returns True if s is a palindrome"""
    s = str(s)
    if (len(s) <= 1) : return True
    elif s[0] != s[-1]: return False
    else: return isPalindrome(s[1:-1])

def fib(n):
    """returns the nth Fibonacci number"""
    n = int(n)
    if (n == 1) or (n == 2): return 1
    else: return fib(n-1)+fib(n-2)

def fib1(n):
    ###uses memoization to calculate nth Fibonacci number, uses global fib_memo dictionary ###
    global fib_memo
    global num_memo_uses
    fib_memo = {0:1,1:1}
    num_memo_uses = 0
    if n in fib_memo:
        num_memo_uses  +=1
        result =  fib_memo[n]
    else:
        result =  fib_internal(n,fib_memo)
        fib_memo[n]=result
    print 'num_memo_uses is ',num_memo_uses
    return result

def fib_internal(n,fib_memo):
    global num_memo_uses
    if n in fib_memo:
        num_memo_uses  +=1
        return fib_memo[n]
    else:
        temp = fib_internal(n-1,fib_memo)+fib_internal(n-2,fib_memo)
        fib_memo[n]=temp
        return temp

def happy():
    """prints the string happy"""
    print 'happy'

    
def factorize(n):
    """takes an integer n and returns a list of all of prime factors ver3"""
    n = long (n)
    i = 2
    while (i <= (n**0.5)):
        if (n % i) == 0 :
            # i is a divisor of n, n is not prime
            return list([i]+factorize(n/i))
        i = i+1
    #n is prime
    return list([n])

def isPrime (n):
    """ takes integer n and returns True if prime otherwise returns False """
    n = int (n)
    if factorize(n) == [n]:
        return True
    else:
        return False

def findCounterExample(n):
    """examines all numbers (2**i)-1 up to i=n for primeness """
    n = int (n)
    for i in range (1,n+1):
        testNumber = (2**i) - 1
        if isPrime(testNumber):
            print testNumber,' is prime'
        else:
            print factorize(testNumber)
##            return(True)
    return (True)

def addTreeElement(n,L):
    """addTreeElement takes an integer n and a 3-element list of the form [sublist1,m,sublist2] where
    each sublist is either an empty list or a 3-element list of similar structure, and all the integers from sublist1
    are less that or equal to m, and all the integers from sublist2 are greater than or equal to m,
    and returns a 3-element list [sublist1a,n,sublist2a] with the above qualifications and that a list of the all
    integers in sublist1a and sublist2a is the same as the list of integers from sublist1, m, and sublist2"""
    if L == []:
        return[[],n,[]]
    elif L[1] > n:
        return [addTreeElement(n,L[0]),L[1],L[2]]
    else:
        return [L[0],L[1],addTreeElement(n,L[2])]
    
def makeTree(L):
    """makeTree takes a list of integers and returns a sorted tree list"""
    tree = []
    for i in range(len(L)):
        tree = addTreeElement(L[i],tree)
    return tree

def flattenTree(L):
    """flattenTree takes a list and flattens it into a simple list"""
    result = []
    if L == []:
        return []
    elif type(L) != type([]):
        return [L]
    else:
        return flattenTree(L[0]) + flattenTree(L[1:])

def treeSort(L):
    """ takes an unsorted list of integers and returns the list of integers sorted in ascending order"""
    return flattenTree(makeTree(L))

def mergeSortedLists(L1,L2):
    """takes two sorted integer lists and returns a single combined sorted list"""
    
    if L1 == [] : return L2
    elif L2 == [] : return L1
    else :
        i,j = 0,0
        result = []
        while (i < len(L1)) and (j < len(L2)):
            if L1[i] < L2[j] :
                result = result + [L1[i]]
                i += 1
            else :
                result = result + [L2[j]]
                j += 1
        if i == len(L1):
            result = result + L2[j:]
        else :
            result = result + L1[i:]
        return result

def mergeSort(L):
    """takes a list and returns a sorted list"""
    if len(L) < 2 :
        return L
    else :
        breakPoint = len(L)/2
        return mergeSortedLists(mergeSort(L[:breakPoint]),mergeSort(L[breakPoint:]))

    
def isElementOfSortedList(n,L):
    """takes sorted list L and determines if n is an element of the list"""
    if L == [] : return False
    else :
        index = len(L)/2
        test = L[index]
        if n == test :
            return True
        elif n > test :
            return isElementOfSortedList(n,L[index+1:])
        else:
            return isElementOfSortedList(n,L[:index])

def mergeIsElementOf(n,L):
    """ determines if integer n is an element of arbitrary list L using merge sort and binary search"""
    return isElementOfSortedList(n,mergeSort(L))


        
def buildConnectionString(params):
    """Build a connection string from a dictionary of parameters.

    Returns string."""
    return ";".join(["%s=%s" % (k, v) for k, v in params.items()])


            
