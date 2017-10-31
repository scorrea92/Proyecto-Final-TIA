#Solución Barcos algoritmo genetico
import os
os.system('clear')

#Inicio del programa
import random
from random import shuffle
import collections
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
mutation_chance = 0.2 #La probabilidad de que un individuo mute
gen = 100 #Numero de generaciones que correra el algoritmo


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
  
def selection_and_reproduction(population):
	"""
	    CrossOver de los individuos. Utilizo la primera mitad de la carga genetica del padre1
	    luego utilizo la carga genetica no repetida de la mitad el padre1 en el padre2 y formo
	    el nuevo individuo
	"""
	puntuados = [ (calcularFitness(i), i) for i in population] #Calcula el fitness de cada individuo
	#Ordena los pares ordenados y se queda solo con el array de valores( max-> acendiente)
	#(min-> descendiente) sorted(, reverse=True)
	puntuados = [i[1] for i in sorted(puntuados, reverse=True)]
	population = puntuados

	selected =  puntuados[(len(puntuados)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'

	#Se mezcla el material genetico para crear nuevos individuos
	for i in range(len(population)-pressure):

		#Se elige un punto para hacer el intercambio
		punto = round(largo/2) #random.randint(1,largo-1) 
		padre = random.sample(selected, 2) #Se eligen dos padres

		#Se mezcla el material genetico de los padres en cada nuevo individuo

		population[i][:punto] = padre[0][:punto]

		padre2 = [x for x in padre[1] if x not in padre[0][:punto]]

		population[i][punto:] = padre2 

	return population #El array 'population' tiene ahora una nueva poblacion de individuos, que se devuelven

def mutation(population):
	"""
	    Se mutan los individuos al azar. Intercambio dos genes de forma aleatoria
	"""
	for i in range(len(population)-pressure):
		if random.random() <= mutation_chance: #Cada individuo de la poblacion (menos los padres) tienen una probabilidad de mutar
			punto1 = random.randint(0,largo-1) #Se elgie un punto al azar
			punto2 = random.randint(0,largo-1)
			while punto1 == punto2:
				punto2 = random.randint(0,largo-1)

			#Se aplica la mutacion
			#print("se ha mutado el idividuo ",i, "y se intercambio ",punto1,punto2)
			aux = population[i][punto1]
			population[i][punto1] = population[i][punto2]
			population[i][punto2] = aux

	return population
	  
#Inicio del proceso de evolucion
  
#population = [[9, 6, 11, 8, 7, 4, 2, 1, 13, 17, 12, 16, 19, 10, 14, 15, 18, 5, 20, 3], [7, 3, 17, 5, 6, 8, 18, 16, 2, 4, 1, 10, 20, 9, 19, 11, 12, 14, 15, 13], [7, 17, 16, 6, 19, 14, 11, 9, 10, 13, 4, 18, 5, 15, 3, 20, 12, 2, 8, 1], [2, 7, 17, 18, 13, 10, 9, 11, 8, 14, 1, 5, 19, 12, 6, 4, 20, 3, 15, 16], [15, 9, 7, 10, 18, 13, 6, 4, 20, 11, 8, 1, 16, 5, 3, 14, 17, 2, 19, 12], [7, 6, 10, 14, 11, 15, 2, 3, 4, 18, 9, 13, 12, 8, 19, 1, 20, 17, 16, 5], [8, 4, 14, 13, 15, 20, 19, 2, 18, 1, 7, 10, 17, 3, 5, 9, 6, 16, 11, 12], [15, 1, 7, 19, 12, 9, 3, 5, 10, 17, 11, 6, 13, 2, 20, 16, 4, 8, 18, 14], [3, 20, 1, 6, 19, 8, 10, 4, 11, 17, 9, 7, 18, 14, 16, 2, 5, 12, 15, 13], [3, 17, 16, 1, 7, 10, 19, 15, 18, 13, 2, 9, 14, 8, 6, 12, 4, 11, 20, 5], [6, 20, 17, 18, 19, 5, 14, 8, 2, 9, 10, 4, 16, 11, 12, 7, 13, 1, 3, 15], [2, 8, 11, 10, 13, 15, 3, 20, 16, 17, 4, 7, 12, 9, 5, 18, 14, 19, 1, 6], [8, 5, 2, 20, 6, 13, 10, 14, 9, 11, 1, 12, 19, 17, 18, 16, 4, 3, 15, 7], [4, 19, 1, 14, 9, 20, 17, 10, 3, 5, 15, 13, 6, 2, 7, 11, 8, 12, 18, 16], [7, 20, 15, 1, 16, 10, 19, 5, 3, 9, 12, 2, 13, 17, 4, 11, 8, 6, 18, 14], [11, 10, 14, 16, 6, 18, 3, 17, 1, 5, 9, 4, 20, 12, 2, 15, 7, 8, 19, 13], [12, 14, 16, 17, 10, 6, 3, 7, 20, 15, 4, 11, 1, 19, 13, 18, 5, 2, 9, 8], [20, 8, 1, 3, 5, 4, 14, 19, 13, 10, 16, 6, 17, 7, 12, 15, 18, 9, 2, 11], [6, 16, 15, 8, 12, 1, 11, 4, 14, 10, 19, 13, 20, 5, 2, 18, 7, 3, 17, 9], [20, 8, 2, 7, 4, 3, 16, 11, 10, 1, 9, 14, 6, 18, 19, 13, 5, 12, 17, 15], [19, 3, 16, 6, 2, 9, 20, 4, 7, 17, 10, 15, 12, 5, 18, 11, 1, 13, 14, 8], [3, 13, 5, 6, 20, 9, 7, 2, 19, 18, 4, 15, 1, 14, 16, 11, 12, 8, 10, 17], [15, 17, 12, 16, 2, 11, 20, 5, 6, 14, 10, 13, 8, 9, 1, 19, 18, 4, 7, 3], [15, 7, 1, 8, 6, 16, 9, 18, 12, 17, 13, 3, 11, 20, 2, 14, 4, 19, 5, 10], [8, 18, 11, 9, 2, 6, 7, 14, 12, 1, 15, 13, 4, 3, 20, 10, 17, 5, 16, 19], [14, 15, 16, 1, 20, 6, 13, 8, 18, 4, 7, 17, 10, 19, 5, 12, 11, 2, 3, 9], [18, 15, 19, 1, 14, 5, 16, 2, 20, 4, 10, 11, 13, 7, 9, 12, 17, 6, 3, 8], [11, 3, 7, 18, 2, 16, 10, 6, 14, 1, 9, 12, 20, 17, 15, 8, 5, 19, 13, 4], [4, 3, 18, 12, 16, 8, 15, 19, 20, 14, 1, 2, 6, 11, 7, 17, 9, 10, 13, 5], [14, 17, 12, 1, 18, 20, 16, 11, 15, 19, 6, 8, 2, 9, 13, 3, 5, 10, 7, 4]]
population = crearPoblacion()#Inicializar una poblacion
puntuados = [ (calcularFitness(i), i) for i in population]
puntuados = [i for i in sorted(puntuados)]
print("Poblacion Inicial:\n%s"%(puntuados)) #Se muestra la poblacion inicial
  
  
#Se evoluciona la poblacion
print("inicio", datetime.now().time())
print("")
for i in range(gen):
	#print("Generacion: ",i)
	population = selection_and_reproduction(population)
	population = mutation(population)

	puntuados = [ (calcularFitness(i), i) for i in population]
	puntuados = [i for i in sorted(puntuados)]
	print(puntuados[0])

print("")
print("Fin", datetime.now().time())
puntuados = [ (calcularFitness(i), i) for i in population]
puntuados = [i for i in sorted(puntuados)]
print("\nPoblacion:\n%s"%(population)) #Se muestra la poblacion evolucionada
print("\n\n")
print("\nPoblacion Final:\n%s"%(puntuados))






