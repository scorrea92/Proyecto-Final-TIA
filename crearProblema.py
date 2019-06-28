#Primer script para crear individuos
import os
os.system('clear')

#Inicio del programa
import random
from random import shuffle

max_barcos = 20
barcos = {}
max_long = 700
max_gruas = 7
FG = max_long/max_gruas

#Creo los 10 barcos de muestra
for i in range(max_barcos):
	mov = round(random.uniform(100, 1000))
	eslora = round(random.uniform(100, 500))
	llegada = round(random.uniform(60,180))
	prioridad = round(random.uniform(0,8))
	barcos[i+1] = [llegada, mov, eslora, prioridad]
print("llegada	mov	eslora	prioridad")
for i in barcos:
	print(i,':',barcos[i])

#Creo matriz de aignamiento de barcos
matrix = [[],[],[],[]]
for i in range(0,200*max_barcos+180):
	matrix[0].append(i+1)
	matrix[1].append([0])
	matrix[2].append(max_long)
	matrix[3].append(max_gruas)

indv = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
shuffle(indv)
print(indv)


print("Inicio de Ejecución")
fitness = 0
#Aca hago la funcion donde llega el individuo y devuelvo el fitness
for barco in indv:
	#print(barcos[barco])
	#calculo el tiempo de atranque
	mov = barcos[barco][1]
	prioridad = barcos[barco][3]
	eslora = barcos[barco][2]
	gruas = round(eslora/FG)
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

print("Fin de Ejecución")
print(fitness)
