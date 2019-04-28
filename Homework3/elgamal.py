from random import randint
from math import gcd, floor

"""Find multiplicative inverse"""
def mult_inv(a, b):
        t, t_prev = 1, 0
        r, r_prev = a, b

        while r != 0:
                q = floor(r_prev / r)
                r_prev, r = r, r_prev - q * r
                t_prev, t = t, t_prev - q * t

        while t_prev < 0:
                t_prev = t_prev + b
        else:
                return t_prev


def get_signature(x, k, alpha, p, a):
    gamma = pow(alpha, k, p)
    multinv_k = mult_inv(k, p-1)
    delta = ((x-a*gamma) *  multinv_k ) % (p-1)
    
    print("Gamma:" +str(gamma), " Delta: " +str(delta))
    return gamma, delta


def verify_signature(x, beta, gamma, delta, alpha, p):
    lhs = (pow(int(beta), int(gamma), p) * pow(int(gamma), int(delta), p)) % p
    print("LHS: " + str(lhs))
    rhs = pow(alpha, x, p)
    print("RHS: " + str(rhs))
    if lhs == rhs:
        print("(Gamma, Delta) is accepted as the signature on m")
    



def main():
    p = 2189284635404723
    alpha = 88 # found in previous question
    a = 685680634326777 # found in previous question
    beta = pow(alpha, a, p)
    m = 186151 #student no. 
    n = 2051152801041163 
    k = 1234567
    # Hash function
    H_f = 8**m % n 
    print("Calculating the signature of m:")
    gamma, delta = get_signature(H_f, k, alpha, p, a)
    print("Verifying the signature:")
    verify_signature(H_f, beta, gamma, delta, alpha, p)

    
main()
     