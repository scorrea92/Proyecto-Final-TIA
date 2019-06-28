#Limpiar la terminal
import os
os.system('clear')

import random
import collections
  
modelo = [6,3,10,7,5,2,8,4,9,1] #Objetivo a alcanzar
largo = 10 #La longitud del material genetico de cada individuo
num = 10 #La cantidad de individuos que habra en la poblacion
pressure = 3 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2
mutation_chance = 1.0 #La probabilidad de que un individuo mute
gen = 100 #Numero de generaciones que correra el algoritmo
  
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
  
def selection_and_reproduction(population):
    """
        CrossOver de los individuos. Utilizo la primera mitad de la carga genetica del padre1
        luego utilizo la carga genetica no repetida de la mitad el padre1 en el padre2 y formo
        el nuevo individuo
    """
    puntuados = [ (calcularFitness(i), i) for i in population] #Calcula el fitness de cada individuo
    #Ordena los pares ordenados y se queda solo con el array de valores( max-> acendiente)
    #(min-> descendiente) sorted(, reverse=True)
    puntuados = [i[1] for i in sorted(puntuados)]
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

        # print(padre[0][:punto])
        # print(padre2)
        # print("")
        #print(population[i])
        
  
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

if __name__ == "__main__":      
    #Inicio del proceso de evolucion
    
    population = crearPoblacion()#Inicializar una poblacion
    print("Poblacion Inicial:\n%s"%(population)) #Se muestra la poblacion inicial
    
    
    #Se evoluciona la poblacion
    for i in range(gen):
        #print("Generacion: ",i)
        population = selection_and_reproduction(population)
        population = mutation(population)

    puntuados = [ (calcularFitness(i), i) for i in population]
    puntuados = [i for i in sorted(puntuados, reverse=True)]
    print("\nPoblacion Final:\n%s"%(puntuados)) #Se muestra la poblacion evolucionada
    print("\n\n")
