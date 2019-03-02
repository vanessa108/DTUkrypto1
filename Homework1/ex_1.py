#!/bin/env python3

from itertools import chain

# Tunables (increase if the key isn't found, at the cost of performance)
TEST_THRESH = 8

# Constants
KEY_BITS = 4
CHARACTER = (0xf, 0xd)
MSG_PAIRS = [
	(
		(0x1, 0xe),
		(0xe, 0x9),
	),
	(
		(0x2, 0x6),
		(0xd, 0xa),
	),
	(
		(0x3, 0x7),
		(0xc, 0xb),
	),
]

S = [0x6, 0x4, 0xc, 0x5, 0x0, 0x7, 0x2, 0xe, 0x1, 0xf, 0x3, 0xd, 0x8, 0xa, 0x9, 0xb]
S_INV = [0x4, 0x8, 0x6, 0xa, 0x1, 0x3, 0x0, 0x5, 0xc, 0xe, 0xd, 0xf, 0x2, 0xb, 0x7, 0x9]

KEYSPACE = range(2 ** KEY_BITS)

TESTER = lambda plain_test, k_seq: S[S[plain_test ^ k_seq[0]] ^ k_seq[1]] ^ k_seq[2]

def guess_keys(msg_pairs, key_num) :
	k = guess_key_cands(MSG_PAIRS, 2)
	
	cases = 0
	
	# Test the Key Candidates
	for k_seq in k :
		plain_test = MSG_PAIRS[0][0][0]
		cipher_test = MSG_PAIRS[0][0][1]
		
		keys_test = TESTER(plain_test, k_seq)
		
		# If two work, we figure we're set. Really we should test all.
		if keys_test == cipher_test and TESTER(MSG_PAIRS[0][1][0], k_seq) == MSG_PAIRS[0][1][1] and TESTER(MSG_PAIRS[1][0][0], k_seq) == MSG_PAIRS[1][0][1] :
			return (cases, k_seq)
			
		else :
			cases += 1
			# ~ print(
				# ~ "TESTED {} == {}:".format(hex(cipher_test), hex(keys_test)),
				# ~ *['k_{}:\t{}'.format(i, hex(k_seq[i])) for i in range(len(k_seq))], sep='\n', end='\n\n'
			# ~ )

def guess_key_cands(msg_pairs, key_num) :
	'''
	Returns list of guesses.
	'''
	
	# The Frequency Counter
	T = [0] * (2 ** KEY_BITS)
	
	for i, k in enumerate(KEYSPACE) :
		for m0, m1 in msg_pairs :
			# We Compute w0 XOR w1 using the formula from differential cryptanalysis.
			w0_w1 = S_INV[m0[1] ^ k] ^ S_INV[m1[1] ^ k]
			
			# Property of Crypto System
			v0_v1 = w0_w1
			
			# Increment Counter
			if v0_v1 == CHARACTER[1] :
				T[i] += 1
	
	# We Grab the Top Eight
	# ~ k = [i for i, x in enumerate(T)]					# Naiive Method. Tests all keys, potentially.
	# ~ k = [i for i, x in enumerate(T) if x == max(T)]		# The key wasn't found in only the maxes :(
	k = [i for i, x in sorted(enumerate(T), key = lambda el: el[1], reverse = True)][:TEST_THRESH]
	
	if key_num == 0 :
		# ~ print(f"Level {key_num}:", k)
		return k
	
	else :
		
		# ~ print(f"Level {key_num}:", k)
		return [
			k_lower + [k_cand] if type(k_lower) == type([]) else [k_lower] + [k_cand]
			for k_cand in k
			for k_lower in guess_key_cands(
				[
					(
						(msg_pairs[i][0][0], S_INV[msg_pairs[i][0][1] ^ k_cand]),
						(msg_pairs[i][1][0], S_INV[msg_pairs[i][1][1] ^ k_cand])
					)
					for i in range(len(msg_pairs))
				],
				key_num - 1
			)
		]

def main() :
	cases, k_seq = guess_keys(MSG_PAIRS, 2)
	
	print(
		f"KEY VALUES {hex(MSG_PAIRS[0][0][0])}:{hex(MSG_PAIRS[0][0][1])} => {hex(TESTER(MSG_PAIRS[0][0][0], k_seq))}",
		*['k_{}:\t{}'.format(i, hex(k_seq[i])) for i in range(len(k_seq))],
		sep='\n',
		end='\n\n'
	)
	
	print(f'Tested {cases} out of {2 ** (KEY_BITS * 3)} Keys')

	
if __name__ == "__main__" :
	main()
