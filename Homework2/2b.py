from math import modf, gcd
from random import randint


""" return true  """
def miller_rabin(m, k):
    #check if m is even
    if m % 2 == 0:
        return False

    t = m - 1 
    s = 0
    while t % 2 == 0:
        t = t / 2 
        s += 1
    # for the number of iterations 
    for _ in range(k):
        b = randint(2, m)
        t = int(t)        
        y = (b**t) % m
        if 1 == y % m: #prime 
            continue       
        else:
            for _ in range(s):
                if -1 == y % m: #prime
                    break            
                else:
                    y = y**2 % m
                    return False
    return True
                       
        


def main():
    # s = 0
    # m = 2
    # k = 1
    # while m < 100: 
    #     is_comp = miller_rabin(m, k)
    #     if is_comp:
    #         m += 1
    #     else: 
    #         s+= 1
    #         m+=1  
    # print(s)

    # if miller_rabin(557, 3): 
    #     print( "m is composite")
    # else:
    #     print("m is prime")
    miller_rabin(7, 5)


if __name__ == "__main__":
    main()