import multiprocessing as mp, time

def f(m):

	while True:
		m.put(1)
		time.sleep(3)

	return

def f2(m):

	while True:
		try:
			print(m.get_nowait())
		except:
			pass
		time.sleep(0.1)
	return

m = mp.Queue()

f = mp.Process(target=f, args=(m,))
f2 = mp.Process(target=f2, args=(m,))
f.start()
f2.start()
