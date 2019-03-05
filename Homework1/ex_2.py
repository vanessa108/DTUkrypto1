#!/bin/env python3

from itertools import chain



# Tunable Constants
NUM_KEYS = 3
CHARACTER = (0xf, 0xd, 0xc)
TESTER = lambda plain_test, k_seq: S[S[S[plain_test ^ k_seq[0]] ^ k_seq[1]] ^ k_seq[2]] ^ k_seq[3]

MSG_PAIRS = [
	(
		(0x0, 0x1),
		(0xf, 0x9),
	),
	(
		(0x1, 0xd),
		(0xe, 0x7),
	),
	(
		(0x2, 0x8),
		(0xd, 0xb),
	),
	(
		(0x3, 0xa),
		(0xc, 0x5),
	),
	(
		(0x4, 0x4),
		(0xb, 0xc),
	),
	(
		(0x5, 0x3),
		(0xa, 0xe),
	),
	(
		(0x6, 0x0),
		(0x9, 0x6),
	),
	(
		(0x7, 0x2),
		(0x8, 0xf),
	),
]

# Constants
S = [0x6, 0x4, 0xc, 0x5, 0x0, 0x7, 0x2, 0xe, 0x1, 0xf, 0x3, 0xd, 0x8, 0xa, 0x9, 0xb]
S_INV = [0x4, 0x8, 0x6, 0xa, 0x1, 0x3, 0x0, 0x5, 0xc, 0xe, 0xd, 0xf, 0x2, 0xb, 0x7, 0x9]

KEY_BITS = 4
KEYSPACE = range(2 ** KEY_BITS)

def guess_keys(msg_pairs, key_num) :
	'''
	Recursively generates key candidates based on
	differential crypanalysis,
	then tests them against all message pairs.
	'''
	
	# Determine Key Candidates
	k = guess_key_cands(msg_pairs, key_num)
	
	# Setup Complexity Analysis & Found Sequence List
	experi_complexity = 0
	k_seqs = []
		
	# Test all Key Sequence Candidates.
	for k_seq in k :
		
		# Test All the Message Pairs & Store as BOolean
		k_seq_test = sum([
			int(TESTER(MSG_PAIRS[i][j][0], k_seq) == MSG_PAIRS[i][j][1])
			for i in range(len(MSG_PAIRS))
			for j in range(2)
		]) == len(MSG_PAIRS) * 2
				
		# If it works, we've found a Key Sequence! Add it!
		if k_seq_test :
			k_seqs.append( k_seq )
		
		# Increment that One Iteration has Happened
		experi_complexity += 1
	
	# Return Tested Correct Key Sequences!
	return (experi_complexity, k_seqs)

def guess_key_cands(msg_pairs, key_num) :
	'''
	Recursively generates key candidates.
	'''
	
	# Initialize the Frequency Counter Array
	T = [0] * (2 ** KEY_BITS)
	
	# Iterate through each Message Pair, for all Keys in the Keyspace.
	for i, k in enumerate(KEYSPACE) :
		for m0, m1 in msg_pairs :
			
			# Normal Case
			if key_num > 0 :
				# Compute (w0 XOR w1) by XOR'ing each with the key, running through the Inverse S-Box, then XOR'ing.
				w0_w1 = S_INV[m0[1] ^ k] ^ S_INV[m1[1] ^ k]
				
				# Just to express that XOR difference before and after the key is the same.
				v0_v1 = w0_w1
				
				# Increment Counter if it matches an appropriate Characteristic
				if v0_v1 == CHARACTER[key_num - 1] :
					T[i] += 1
					
			# Special Case to find Key 0
			if key_num == 0 :
				# Ignore the S-Box Inversion
				m0_m1 = (m0[1] ^ k) ^ (m1[1] ^ k)
				
				# Increment Counter if it matches an appropriate Characteristic
				if m0_m1 == CHARACTER[key_num] :
					T[i] += 1
					
				# NOTE: We really should XOR the given plaintext m with the u (eg. m0[1] or m1[1] XORed with m0[0] or m1[0])
	
	
	# Choose Keys (indices) by Filtering the Frequency Array
	# ~ k = [i for i, x in enumerate(T)]						# Brute Force
	k = [i for i, x in enumerate(T) if x == max(T)]				# More clever, might miss keys.
	
	# IDEA: We could choose & test the most statistically significant (thresholded) high-frequency elements!
	
	
	# Base Case
	if key_num == 0 :
		return k
	
	# Recursive Case
	else :
		# Accumulate All Permutations of Key Sequences & Return
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
	# Guess the Keys & Experimental Iterations that it Took
	exp_iterations, k_seqs = guess_keys(MSG_PAIRS, NUM_KEYS)
	
	# Display Found Key Sequences w/Trivial Test Result
	for k_seq in k_seqs :
		given_plain = hex( MSG_PAIRS[0][0][0] )
		given_cipher = hex( MSG_PAIRS[0][0][1] )
		found_cipher = hex( TESTER(MSG_PAIRS[0][0][0], k_seq) )
		
		print(
			f"KEY VALUES {given_plain} => {given_cipher} <-> {found_cipher}",
			*[f"Key {i}:\t{hex(k_seq[i])}" for i in range(len(k_seq))],
			sep='\n',
			end='\n\n'
		)
	
	# Display Complexity Analysis
	print(
		f'Tested {exp_iterations} Keys out of {2 ** (KEY_BITS * NUM_KEYS)}',
		f'({( 2 ** (KEY_BITS * NUM_KEYS) ) / exp_iterations}x Faster than Brute Force)'
	)

	
if __name__ == "__main__" :
	main()
