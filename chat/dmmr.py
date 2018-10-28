import random

results = []

def games(qant, mmr, prob):

	for e in range(0, qant):

		if random.random() <= prob:
			mmr += 25
		else:
			mmr -= 25

		print(mmr, end=" ", flush=True)
	print('\n', mmr)
	results.append(mmr)

for e in range(0, 9):
	games(1000, 3600, .5)

print(results)