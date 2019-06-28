#Solución Barcos algoritmo genetico
import os
os.system('clear')

#Inicio del programa
import random
from random import shuffle
import collections
import math
from datetime import datetime
#Formato de información de barcos	
max_barcos = 20
barcos = {}
max_long = 700
max_gruas = 7
FG = max_long/max_gruas

#Creo los 10 barcos de muestra
# for i in range(max_barcos):
# 	mov = round(random.uniform(100, 1000))
# 	eslora = round(random.uniform(100, 500))
# 	llegada = round(random.uniform(30,180))
# 	prioridad = round(random.uniform(0,8))
# 	barcos[i+1] = [llegada, mov, eslora, prioridad]
barcos = {1: [100, 390, 375, 3], 2: [84, 700, 414, 6], 3: [38, 706, 149, 1], 4: [51, 352, 500, 5], 5: [59, 745, 285, 6], 6: [102, 565, 139, 6], 7: [115, 308, 453, 6], 8: [154, 713, 438, 6], 9: [113, 889, 150, 7], 10: [152, 466, 388, 6], 11: [77, 176, 119, 3], 12: [46, 788, 468, 6], 13: [133, 517, 174, 7], 14: [168, 787, 277, 3], 15: [71, 309, 498, 0], 16: [66, 990, 419, 4], 17: [122, 595, 177, 6], 18: [168, 858, 117, 2], 19: [96, 406, 447, 4], 20: [60, 223, 455, 1]}

print("llegada	mov	eslora	prioridad")
for i in barcos:
	print(i,':',barcos[i])

largo = max_barcos #La longitud del material genetico de cada individuo
num = 30 #La cantidad de individuos que habra en la poblacion
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
gen = 100 #Numero de generaciones que correra el algoritmo
T = 10000 #Temperatura inicial
k = 0.1 #

def individual(min, max):
	"""
	    Crea un individual
	"""
	return random.sample(range(min,max+1), largo)

def crearPoblacion():
	"""
	    Crea una poblacion nueva de individuos
	"""
	return [individual(1,largo) for i in range(num)]
  
def calcularFitness(individual):
	"""
	    Calcula el fitness de un individuo concreto. 
	"""
	#Creo matriz de aignamiento de barcos
	matrix = [[],[],[],[]]
	for i in range(0,200*max_barcos+180):
		matrix[0].append(i+1)
		matrix[1].append([0])
		matrix[2].append(max_long)
		matrix[3].append(max_gruas)

	fitness = 0
	#Aca hago la funcion donde llega el individuo y devuelvo el fitness
	for barco in individual:
		#print(barcos[barco])
		#calculo el tiempo de atranque
		mov = barcos[barco][1]
		prioridad = barcos[barco][3]
		eslora = barcos[barco][2]
		gruas = round(eslora/FG)+1
		t_llegada = barcos[barco][0]
		t_atranque = round(mov/gruas)

		#Evalua las siguientes condiciones

		vacia = 0
		bool_gruas = True
		bool_longm = True
		for i in range(0, t_atranque):
			vacia += len(matrix[1][t_llegada-1:t_llegada+t_atranque][i])==1
			bool_gruas = bool_gruas and (matrix[2][t_llegada-1+i]>=gruas)
			bool_longm = bool_longm and (matrix[2][t_llegada-1+i]>=eslora)

		#Evaluo el estado del puerto vacio, con espacio, o sin espacio
		if(vacia == t_atranque or (bool_gruas and bool_longm)):
			#Si esta vacia o hay espacio de longitud y gruas ubico el barco en dicha posición
			for i in range(0, t_atranque):
				matrix[1][t_llegada-1:t_llegada+t_atranque][i].append(barco)
				matrix[2][t_llegada-1+i] = matrix[2][t_llegada-1+i] - eslora
				matrix[3][t_llegada-1+i] = matrix[3][t_llegada-1+i] - gruas

			tiempo_espera = 0

			fitness = fitness + prioridad*tiempo_espera + (1-prioridad)*t_atranque
		else:
			#Si no esta vacia comienzo a moverme de a 1 minuto en el tiempo para ubicarlo lo mas
			#cercano posible
			t_lledada_0 = t_llegada
			while True:
				t_llegada += 1
				bool_gruas = True
				bool_longm = True
				for i in range(0, t_atranque):
					bool_gruas = bool_gruas and (matrix[2][t_llegada-1+i]>=gruas)
					bool_longm = bool_longm and (matrix[2][t_llegada-1+i]>=eslora)
				if ((bool_gruas and bool_longm)):

					tiempo_espera = t_llegada - t_lledada_0
					fitness = fitness + prioridad*tiempo_espera + (1-prioridad)*t_atranque
					break	
		
			for i in range(0, t_atranque):
				matrix[1][t_llegada-1:t_llegada+t_atranque][i].append(barco)
				matrix[2][t_llegada-1+i] = matrix[2][t_llegada-1+i] - eslora
				matrix[3][t_llegada-1+i] = matrix[3][t_llegada-1+i] - gruas
		
		#Donde sobren gruas se las distribuyo entre todos los barcos ubicados

	return fitness

def enfriamiento(population):
	"""
		Se realiza el enfriamiento a cada individuo
	"""
	global Tv
	global k
	for i in range(len(population)):
		new = list(population[i])
		old = list(population[i])
	
		punto1 = random.randint(0,largo-1) #Se elgie un punto al azar
		punto2 = random.randint(0,largo-1)

		aux = new[punto1]
		new[punto1] = new[punto2]
		new[punto2] = aux

		deltaF = calcularFitness(old) - calcularFitness(new)
		prob = math.exp( deltaF/Tv[i] )

		# print("old",old)
		# print("new",new)
		
		# print("Fitness viejo",calcularFitness(old))
		# print("Fitness nuevo",calcularFitness(new))
		
		# print("Delta",deltaF)
		# print("Prob",prob)
		# print("T",T)

		if(deltaF>=0):
			population[i] = new
			Tv[i] = Tv[i]/(1+k*(Tv[i]/10000))
		else:
			if(random.random() <= prob):
				population[i] = new
			else:
				population[i] = old

	return population


if __name__ == "__main__":
	#Inicio del proceso de evolucion

	population = [[4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 11, 10, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 8, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 10, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 15, 20], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 19, 17, 2, 1, 5, 13, 6, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 3, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 6, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15], [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15]]
	#population  = crearPoblacion()#Inicializar una poblacion
	puntuados = [ (calcularFitness(i), i) for i in population]
	puntuados = [i for i in sorted(puntuados)]
	print("Poblacion Inicial:\n%s"%(puntuados)) #Se muestra la poblacion inicial
	Tv = [ T for i in population]
	print("inicio", datetime.now().time())
	print("")
	#Se realiza el enfriamiento con iteraciones
	for i in range(gen):
		print("Iteracion: ",i)
		population = enfriamiento(population)
		puntuados = [ (calcularFitness(i), i) for i in population]
		puntuados = [i for i in sorted(puntuados)]
		print("T: ",Tv)
		print("Mejor fitness ",puntuados[0])


	# #Se realiza el enfriamiento con T minimo
	# i=0
	# while (T > 1000):
	# 	print("T",i,": ",T)
	# 	population = enfriamiento(population)
	# 	i+=1
	print("")
	print("Fin", datetime.now().time())
	print("")
	puntuados = [ (calcularFitness(i), i) for i in population]
	puntuados = [i for i in sorted(puntuados)]
	print("\nPoblacion:\n%s"%(population)) #Se muestra la poblacion evolucionada
	print("\n\n")
	print("\nPoblacion Final:\n%s"%(puntuados))
