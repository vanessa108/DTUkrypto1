
from random import randrange

def miller_rabin(n, k):
	if n == 2:
		return True
	if not n & 1:
		return False

	def check(a, s, d, n):
		x = pow(a, d, n)
		if x == 1:
			return True
		for i in range(s - 1):
			if x == n - 1:
				return True
			x = pow(x, 2, n)
		return x == n - 1

	s = 0
	d = n - 1

	while d % 2 == 0:
		d >>= 1
		s += 1

	for i in range(k):
		a = randrange(2, n - 1)
		if not check(a, s, d, n):
			return False
	return True

def main():
	m = 25
	k = 1
	s = 0
	while m < 25000:
		if miller_rabin(m, k):
			s += 1
		m += 1
	print(s)
    # if miller_rabin(13, 3):
    #     print("prime")
    # else:
    #     print("composite")

if __name__ == "__main__":
    main()