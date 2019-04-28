from math import sqrt

""" Verifies if a number is prime using trial division
    Returns true if number is a prime """
def trial_division(m):
    r = 2
    while r <= sqrt(m):
        if m % r == 0: 
            return False
        else:
            r += 1
    return True

def main():
    # s counts the number of primes found
    s = 0
    # for all numbers between 25 and 25000 (26 to 24999)
    m = 25 + 1
    while m < 25000: 
        #if m is a prime, increase the counter s 
        if trial_division(m):
            s += 1
        #increment m by 1 to test the number         
        m+=1   
    #once all values for m have been tested, print the number of primes counted
    print("The number of primes between 25 and 25000 is " + str(s))
    
                

if __name__ == "__main__" :
    main()