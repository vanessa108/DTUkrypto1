from math import floor, gcd

""" Returns the multiplicative inverse of two numbers, based of Extended Euclidean Algorithm psuedo code from
https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode"""

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

"""Finds the values for phi_n and psi_n"""
def find_values(p, q):
    phi = (p-1) * (q-1)
    psi = phi / gcd(p - 1, q -1)
    return phi, psi

def main():
    #set values    
    p = 881
    q = 461
    e = 3
    phi_n, psi_n = find_values(p, q) 
    d1 = mult_inv(e, phi_n)
    d2 = mult_inv(e, psi_n)
    print("The greatest common divisor of e and phi_n is " + str(gcd(e, phi_n)))
    print("The value for d1 is " + str(d1))
    print("The value for d2 is " + str(d2))



    

    
if __name__ == "__main__" :
	main()