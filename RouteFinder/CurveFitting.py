# Module for testing statistics

import pylab

def rsquared(measured,estimated):
    diffs = (measured-estimated)**2
    mmean=measured.sum()/float(len(measured))
    var = (mmean - measured)**2
    return 1 - diffs.sum()/var.sum()

x=[1,2,3,4,5,6]
y=[1.1,1.9,3.1,3.9,5.1,5.9]
y2=[1.5,3.5,9.5,15.5,25.5,36.5]

x=pylab.array(x)
y=pylab.array(y)
y2=pylab.array(y2)

a,b = pylab.polyfit(x,y,1)
print ' a is',a,'b is ',b
estimated = a*x + b
print 'rsquared for linear problem is ',rsquared(y,estimated)

pylab.plot(x,y)
pylab.plot(x,estimated)

pylab.figure()
a,b,c = pylab.polyfit(x,y2,2)
print ' a is',a,'b is ',b,'c is ',c
estimated = a*x**2 + b*x + c
print 'rsquared for quadratic problem is ',rsquared(y2,estimated)

pylab.plot(x,y2)
pylab.plot(x,estimated)

pylab.show()
