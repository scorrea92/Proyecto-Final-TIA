# Proyecto-Final-TIA

El problema descrito es una lista de espera de barcos para el atraque en una terminal de contenedores.

![Image of problem](https://raw.githubusercontent.com/scorrea92/Proyecto-Final-TIA/master/resources/Imagen%201.png)

## Método de Solución

* Cada individuo está compuesto por una posible combinación de los N barcos del problema [15 2 3 10 9 8……] (1-20). 
* La población está formada por un número x de individuos y se puede iniciar de forma aleatoria o fija.
* Para la reproducción se utilizó la primera mitad de la carga genética del padre1 luego se utilizó la carga genética no repetida del padre1 de la mitad del padre2 para formar el nuevo individuo. 
* La mutación y los vecinos se realizaron como un cambio aleatorio de genes en los individuos de la población.

## Resultados

![comparativa](https://raw.githubusercontent.com/scorrea92/Proyecto-Final-TIA/master/resources/Imagen_2.png)


## Concluciones

* Para el problema planteado el algoritmo genético presenta mejores resultados que el algoritmo de enfriamiento simulado. El mejor individuo obtenido en todos los experimentos para la solución del problema fue:
    [4, 7, 10, 11, 9, 6, 17, 2, 1, 5, 13, 19, 12, 8, 18, 16, 14, 3, 20, 15]

* En un caso práctico de necesitarse detener el algoritmo debido a cuestiones de tiempo y necesidad y trabajar con la última solución obtenida el algoritmo genético asegura que el individuo que entregara será mejor al anterior y a la inicial, mientras que en el enfriamiento simulado como hay una búsqueda de mejora la solución podría encontrarse en una desmejora en comparación con su solución anterior o inicial

#### Para más información ver [memoria]()