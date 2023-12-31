
# A simple demo of Frievalds algorithm on two matrices of size n


import numpy as np

def Frievalds_check(A,B,C,n):
    prime=(2**n)-1
    r=np.random.randint(prime)
    x=np.array([(r^i)%prime for i in range (n)])
    return np.all(np.matmul(C,x)==np.matmul(A,np.matmul(B,x)))

n=3
if Frievalds_check(np.random.random((n,n)),np.random.random((n,n)),np.matmul(A,B),n):
    print('equal')
else:
    print('Not equal')
