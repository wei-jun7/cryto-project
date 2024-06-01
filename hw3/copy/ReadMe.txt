Xinning Wang
Rin: 661996169
Rcs: wangx50

#----------------------------------------------------------------------
q1
first get Bob's public key PB
then calculate what Alice send Bob (C1,C2) where C1 = k * G, C2 = Pm + (k * PB)
And when Bob decrypts the message, we have M = C2 - (k * NB * C1)

#----------------------------------------------------------------------
q2
J(x,p) equivalent to 0 if x equivalent to 0 mod p

J(x,mn) = J(x,m) * J(x,n)

J(x,n) 
if x mod 2 = 0:
    if ((n^2 - 1) / 8) mod 2 = 0:
        J(x,n) = J(x/2,n)
    else:
        J(x,n) = -J(x/2,n)
else:
    if ((x-1)(n-1) / 4) mod 2 = 0:
        J(x,n) = J(n mod x, x)
    else:
        J(x,n) = -J(n mod x, x)



#----------------------------------------------------------------------
q3
So bascially just copy the algorithm from the slides (CrypoSec_L7.pdf)
I also do not change most of the variable name from it
For the message part, I guest it's just converting the message to binary form, that's 6*8 = 48 bits total
So calculating h from it: log2(log2(m)) = 4, meaning every block has 4 bits, I do not put that process in the program.
So when it comes to get the last four significant bits in string, it's bin(xi & 15)[2:].zfill(4)
Note that if for other calculates, the first 15(2^4-1) and last 4 need to be modified
And also for calculating a and b: -57*499 + 52*547 = 1

For sending the encrypted message, I use an array to represent c1c2c3....ct, 
and a tuple outside the array to also include x_(t+1) which I name it xt1 in the program.

For the result, I compare the array m1m2m3...mt with the original splited m

SO the content show in your terminal should be:
1. tuple of the encrypted message and x_(t+1) (ciphered_message, x_(t+1))
2. array of the original splitted message
3. array of the dycrypted message


#----------------------------------------------------------------------
q4a
Same as the slides, having KU = (e,n) KR = (d,p,q)
Ci = Mi ^ e mod n
Mi = Di = Ci ^ d mod n

q4b
for r being the random 8 bits number,
Using C = (y1,y2) = (r ^ e mod n, M xor H(r)) to encrypt
and to decrypt, first compute r = y1 ^ d mod n, and M = y2 xor H(r)

the only difference is that we did two rounds of encryption here with the same r, 
for maintaining semantic security, each encryption operation should be unique.
so I generate two DES keys key1 and key2
and thus y2 = ((M xor H1(r)) xor H2(r))
and then for decryption, M = ((y2 xor H2(r)) xor H1(r))

#----------------------------------------------------------------------
utils2.py is the simplified DES implement from hw1,where I use it in q4b in calculating hash values
