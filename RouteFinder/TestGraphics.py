# test pylab graphics

from pylab import *
import random

##pylab.figure()
####x=arange(0,10,0.2)
####y=sin(x)
####plot(x,y)
####ylabel('Value of sin(x)')
####xlabel('Value of x')
####title('My Graph')
##
##
###create big-expensive-figure
##ioff() # turn updates off
##title('now how much would you pay?')
####xticklabels(fontsize=20, color='green')
##draw() # force a draw
##savefig('alldone', dpi=300)
##close()
##ion() # turn updating back on
##plot(rand(20), mfc='g', mec='r', ms=40, mew=4, ls='--', lw=3)


##show()


verts = [(1.,0.),(.5,.8),(-.5,.8),(-1.,0.),(-.5,-.8),(.5,-.8),(1.,0.),]
x = array((1,.5,-.5,-1,-.5,.5,1))
y = array((0,.8,.8,0,-.8,-.8,0))
figure()
plot(x,y)
axvline(0.5, label = 'a vertical line')
axhline(0.5, label = 'a horizontal line')
axis([-3,3,-2,2])
ylabel('Value of sin(x)')
xlabel('Value of x')
title('My Graph')

figure()
scatter(x,y)

figure()
vals = []
dieVals = [1,2,3,4,5,6]
for i in range(10000):
    vals.append(random.choice(dieVals)+random.choice(dieVals))
hist(vals,bins=11)

##import matplotlib.pyplot as plt
##from matplotlib.path import Path
##import matplotlib.patches as patches
##verts = [
##(0., 0.), # left, bottom
##(0., 1.), # left, top
##(1., 1.), # right, top
##(1., 0.), # right, bottom
##(0., 0.), # ignored
##]
##codes = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY,]
##path = Path(verts, codes)
##fig = plt.figure()
##ax = fig.add_subplot(111)
##patch = patches.PathPatch(path, facecolor='white', lw=1)
##ax.add_patch(patch)
##ax.set_xlim(-2,2)
##ax.set_ylim(-2,2)
show()


