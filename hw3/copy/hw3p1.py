# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:40:49 2024

@author: zhonge
"""

class Point:  
    def __init__(self , x=0 , y=0):
        self.x = x
        self.y = y
    
    def __eq__(self , p1):
        return p1.x == self.x and p1.y == self.y
    
    def copy(self):
        return Point(self.x , self.y);
    
    def __str__(self):
        return "({} , {})".format(self.x , self.y)
    
    def negate(self):
        self.y = -self.y
    
    
class EllipticCurve:
    def __init__(self , a , b , mod , generator_pt = None):
        self.a =a
        self.b = b
        self.mod = mod
        self.generator_pt = generator_pt
    
    #returns p1 + p2 on a finite ec
    def add(self , p1 , p2):
        if p1 == p2:
            top = 3 * (p1.x ** 2) + self.a
            bottom = 2 * p1.y
        else:
            top = p2.y - p1.y
            bottom = p2.x - p1.x
        m = top * pow(bottom , -1 , self.mod)
        x3 = (m ** 2 - p1.x - p2.x) % self.mod
        y3 = (m * (p1.x - x3) - p1.y) % self.mod
        return Point(x3 , y3);
    
    #returns c * p1 on a finite ec
    def mul(self , p1 , c):
        ans = p1.copy()
        for i in range(1 , c):
            ans = self.add(ans , p1)
        return ans;
    
ec1 = EllipticCurve(0 , -4 , 257 , Point(2 , 2))
private_key_alice = 41
private_key_bob = 101
public_key_alice = ec1.mul(ec1.generator_pt , private_key_alice)
public_key_bob = ec1.mul(ec1.generator_pt , private_key_bob)
plaintxt = Point(112 , 26)
cipher_txt2 = ec1.add(plaintxt , ec1.mul(public_key_bob , private_key_alice))
print("plaintxt is" , plaintxt)
print("Alice's public key is" , public_key_alice)
print("Bob's public key is" , public_key_bob)
print("ciphertxt is {{{} , {}}}".format(public_key_alice , cipher_txt2))
print("Decrypting message:")
tmp = ec1.mul(public_key_alice , private_key_bob)
tmp.negate() #tmp = -nkg
deciphered_plaintxt = ec1.add(cipher_txt2 , tmp)
print("Decrypted msg is" , deciphered_plaintxt)
        