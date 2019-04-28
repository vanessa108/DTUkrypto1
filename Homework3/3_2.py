from random import randint

p = 2189284635404723

def find_alpha(p):
    q = (p) // 2
    for alpha in range(100):
        #pow(a, b, c) = a^b % c 
        if pow(alpha, 2, p) != 1:
            if pow(alpha, q, p) != 1:
                print(alpha)


def find_a(p):
    a = randint(0, p - 1)
    print(a)


def main():
    p = 2189284635404723
    print("Primitive elements mod P:")
    find_alpha(p) #88
    print("Private key a:")
    find_a(p) #685680634326777



main()
