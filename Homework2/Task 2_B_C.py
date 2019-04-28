from math import modf, gcd
from random import randrange

""" Miller Rabin primality for one iteration, returns true if probably prime"""
def prime_test(m, b, s, t):
        # y = b^t mod m
        y = pow(b, int(t), m)
        if y % m == 1: #probably prime
            return True
        else:
            i = 0
            for _ in range(s-1):
                if y == m - 1: #probably prime
                    return True
                #y = y^2 mod m
                i += 1
                y = pow(y, 2, m) 
            #determine if the prime condition was satisfied and return true, 
            # otherwise returns false (composite)       
            if (y == m-1):
                return True
            else:
                return False

""" Miller rabin for k iterations, returns true if probably prime  """
def miller_rabin(m, k):
    #check if m is even
    if m % 2 == 0:
        return False #composite
    #calculate t and s values
    t = m - 1 
    s = 0
    while t % 2 == 0:
        t = t/2
        s += 1
    #call the Miller Rabin for one iteration k times
    for _ in range(k):
        #generate a new b value each time
        b = randrange(2, m-1)
        if not prime_test(m, b, s, t):
            return False #composite
    return True #prime

"""Finds the number of primes in a defined range"""               
def primes_in_range(lower, upper, k, s):
    while lower < upper:
        if miller_rabin(lower, k):
            s+=1 #increase counter for primes
        lower+=1 #increase number being tested 
    print(str(k) + " iteration(s):", s)

def main():
    #number of iterations tested
    for i in range(1,5):
        s = 0
        primes_in_range(25, 25000, i, s)
    


if __name__ == "__main__":
    main()