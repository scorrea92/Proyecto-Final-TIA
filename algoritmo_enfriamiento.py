#Enfriamiento simulado
import os
os.system('clear')

import random
import collections
import math
  
modelo = [6,3,10,7,5,2,8,4,9,1] #Objetivo a alcanzar
largo = 10 #La longitud del material genetico de cada individuo
num = 3 #La cantidad de individuos que habra en la poblacion
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
gen = 3 #Numero de generaciones que correra el algoritmo
T = 10000 #Temperatura inicial
k = 0.1 #
  
print("\n\nModelo: %s\n"%(modelo)) #Mostrar el modelo
  
def individual(min, max):
    """
        Crea un individual
    """
    return random.sample(range(min,max+1), largo)
  
def crearPoblacion():
    """
        Crea una poblacion nueva de individuos
    """
    return [individual(1,10) for i in range(num)]
  
def calcularFitness(individual):
    """
        Calcula el fitness de un individuo concreto.
    """
    fitness = 0
    for i in range(len(individual)):
        if individual[i] == modelo[i]:
            fitness += 1
  
    return fitness
      
def enfriamiento(population):
    """
        Se realiza el enfriamiento a cada individuo
    """
    i=0
    for ind in population:
        print(i)
        print(ind)
        for p in range(0,largo-1):
            newind = ind
            aux = newind[p]
            newind[p] = newind[p+1]
            newind[p+1] = aux
            print(newind)

            deltaF = calcularFitness(ind) - calcularFitness(newind)
            print("Fitness viejo",calcularFitness(ind))
            print("Fitness nuevo",calcularFitness(newind))
            prob = math.exp( deltaF/T )
            print("Delta",deltaF)
            print("Prob",prob)
            if(deltaF>=0):
                population[i] = newind
            else:
                if(random.random() <= prob):
                    population[i] = newind


        i +=1

    return population

if __name__ == "__main__":
    #Inicio del proceso de evolucion
    
    population = crearPoblacion()#Inicializar una poblacion
    puntuados = [ (calcularFitness(i), i) for i in population]
    puntuados = [i for i in sorted(puntuados)]
    print("Poblacion Inicial:\n%s"%(puntuados)) #Se muestra la poblacion inicial
    
    
    #Se realiza el enfriamiento
    for i in range(gen):
        #print("Generacion: ",i)
        population = enfriamiento(population)
        T = T/(1+k*T)

    puntuados = [ (calcularFitness(i), i) for i in population]
    puntuados = [i for i in sorted(puntuados)]
    print("\nPoblacion Final:\n%s"%(puntuados)) #Se muestra la poblacion evolucionada
    print("\n\n")
