import itertools

print("------inicio-------")
def fizzBuzz():
	fizz = "fizz"
	buzz = "buzz"
	counter = 1
	while True:

		divisivel3 = counter % 3 == 0
		divisivel5 = counter % 5 == 0
		
		if divisivel3 and divisivel5:
			yield fizz + " " + buzz
		elif divisivel3:
			yield fizz
		elif divisivel5:
			yield buzz
		else:
			yield str(counter)
		
		counter += 1

for valor in itertools.islice(fizzBuzz(), 15):
	print(valor)

print("------fim-------")

