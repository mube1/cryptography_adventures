import des

plain='0123456789ABCDEF'
key='133457799BBCDFF1'


M = '0000 0001 0010 0011 0100 0101 0110 0111 1000 1001 1010 1011 1100 1101 1110 1111'.replace(' ', '')
L = '0000 0001 0010 0011 0100 0101 0110 0111'.replace(' ', '')
R = '1000 1001 1010 1011 1100 1101 1110 1111'.replace(' ', '')
cipher='85E813540F0AB405'

# print(R)
shifts=16*[2]
shifts[:2]=[1,1]
shifts[8]=1
shifts[-1]=1
# print(shifts)



"""
DES algorithm  https://page.math.tu-berlin.de/~kant/teaching/hess/krypto-ws2006/des.htm
-make sure message is in hex, and len(message_hex) must be multiple of 64 bits
-pad message to be a multiple of 64 bits
- generate 16 sub-key pairs of length 48 bit
- 

"""
PC_1='57 49 41 33 25 17 9 1 58 50 42 34 26 18 10 2 59 51 43 35 27 19 11 3 60 52 44 36 63 55 47 39 31 23 15 7 62 54 46 38 30 22 14 6 61 53 45 37 29 21 13 5 28 20 12 4'
p=[57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36,63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
hexify={'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111', '8': '1000', '9': '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'}
key_binary=''.join([hexify[i] for i in key])

# print('key in binary ',key_binary, len(p))

pc_key=''.join([key_binary[i-1] for i in p])

# print('permuted key ',pc_key, len(pc_key))

def shifter(string,step):
    return string[step:]+string[:step]
c,d=[],[]
c.append(pc_key[:28])
d.append(pc_key[28:])


# print(c[-1],shifter(c[-1],shifts[0]))



permuted_keys=[]
for i,indx in enumerate(range(1,17)):
#     # shift=shifts[i]
    # print((i+1),c[-1],d[-1])

    c.append(shifter(c[-1],shifts[indx-1]))
    d.append(shifter(d[-1],shifts[indx-1]))
    permuted_keys.append(c[-1]+d[-1])

########################  PC-2 ######
# print(des.key_PBox)
New_permuted_keys=[]
# print(permuted_keys[0])
# print(''.join([ permuted_keys[0][i-1] for i in des.key_PBox]))
for pk in permuted_keys:
    New_permuted_keys.append(''.join([pk[i-1] for i in des.key_PBox]))

# print(New_permuted_keys)
# print(plain)
plain_binary=''.join([hexify[i] for i in plain])
# print(plain_binary)

########################  PC-2 ######
IPed_message=''.join([plain_binary[i-1] for i in des.IP])
# print(IPed_message)
import numpy as np

def bin_operation(str_1,str_2):
    
    f=np.array(list(map(lambda i:i[0]!=i[1],zip(str_1,str_2))))*1
    res=[]
    for i in f:
        if i:
            res.append('1')
        else:
            res.append('0')
    return ''.join(res)



L,R=[],[]
L.append(IPed_message[:32])
R.append(IPed_message[32:])

def s_box(six_bit,index):
    row=int(six_bit[0]+six_bit[1],2)
    column=int(six_bit[1:-1], 2)    
    SBOX=des.SBox_2[index]
    b=bin(SBOX[row][column])[2:]
    b=(4-len(b))*'0'+b
    return b

def f(right,k):
    # print(right)
    # E: expand using a talbe from 32 to 48
    expander=des.EBox
    new_x=''.join([right[i-1] for i in expander])
    pre_s_box=bin_operation(new_x,k)
    # print(pre_s_box)
    # print()
    #works fine
    separator=lambda x: [x[0:6],x[6:12],x[12:18],x[18:24],x[24:30],x[30:36],x[36:42],x[42:]]
    separated=separator(pre_s_box)
    # print(separated)
    r=[ s_box(separated[i],i) for i in range(8)]
    # print('s - boxed ',r,len(r))
    r=''.join(r)

    # print()
    # final permuation
    F_PBox=des.F_PBox
    final=''.join([r[i-1] for i in F_PBox])

    return final



for counter,key in enumerate(New_permuted_keys):    
    L.append(R[-1])
    R.append(bin_operation(L[-2],f(R[-1],key)))    
    # print(counter,' ',L[-1],R[-1])

# reversed 
Cipher=R[-1]+L[-1]

Cipher=''.join([Cipher[i-1] for i in des.FP])
print(hex(int(Cipher, 2))[2:])


