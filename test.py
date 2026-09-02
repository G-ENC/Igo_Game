from numpy import * 
import copy 

a = [2, 6, 9, 4]
print(id(a))

b = a.copy() 
print(id(b))

a[1] = 7       
print(a)
print(b)

if (a==b):
    print("same content")