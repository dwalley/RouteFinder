# File I/O testing


from __future__ import print_function
import fileinput

for line in fileinput.input('testfile.txt'):
    print(type(line))
    print (line)

f=open('testoutput.txt','a')
print('This is the output',file=f)
f.close()

