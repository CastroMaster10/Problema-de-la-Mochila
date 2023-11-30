import timeit
from openpyxl import load_workbook
from tabulate import tabulate
import statistics
import matplotlib.pyplot as plt
import seaborn as sns
import csv

sns.set()

class Contenedor:
    def __init__(self,profit,weight):
        self.profit = profit
        self.weight = weight
    

def carguero_problema(capacidad,items):

    #Ordenamos los contenedores en base al radio de: Beneficio / Peso
    items.sort(key=lambda x:x.profit / x.weight,reverse = True)

    totalProfit = 0 #total profit
    iteraciones = 0 #guardar el numero de iteraciones

    for item in items:
        if capacidad >= item.weight:
            #Si tenemos capacidad de cargar el contenedor, lo hacemos
            totalProfit += item.profit * item.weight
            capacidad -= item.weight
            iteraciones += 1
        else:
            break
    
    return totalProfit,iteraciones

#operaciones: n log n + n + 1 + 1
#Complejidad: O(n log n) worst case scenario


def crearCargueros():
    workbook = load_workbook(filename="mochila_1.xlsx")

    # Get the first sheet.
    worksheet = workbook.worksheets[0]

    # Convert the sheet to a list of lists.
    data = [[cell.value for cell in row] for row in worksheet]

    pesos = []
    beneficios = []
    
    for i in range(len(data)):
        if data[i][0] == 'Contenedor':
            continue
        elif data[i][0] == 'Peso':
            pesos_carguero = []
            for j in range(1,len(data[i])):
                if data[i][j] == None:
                    break
                pesos_carguero.append(data[i][j])
            pesos.append(pesos_carguero)
        
        elif data[i][0] == 'Beneficio [$/ton]':
            beneficios_carguero = []
            for j in range(1,len(data[i])):
                if data[i][j] == None:
                    break
                beneficios_carguero.append(data[i][j])
            beneficios.append(beneficios_carguero)

        elif data[i][0] == None:
            continue
    
    cargueros = {}
    #Ingresar los primeros datos
    #cargueros["carguero0"] = [[100,155,50,112,70,80,60,118,110,55],[1741,1622,1016,1264,1305,1389,1797,1330,1559,1578]]
    for i in range(len(pesos)):
        cargueros['carguero' + str(i)] = [pesos[i],beneficios[i]]
    
    return cargueros



def solucionarProblema():
    datos_cargueros = crearCargueros()
    capacidadMax = 700 #capacidad maxima de cada carguero
    table_data = [["Carguero","Valor objetivo (optimo)","Valor objetivo (heuristico)","Tiempo de computo heuristico(s)","Aprox porcentual del heuristico con respecto al modelo","Proporcion de tiempo de ejecucion de heuristico con respecto al modelo"]]
    nombres_cargueros =  []
    objetivos = []
    tiempos = []
    aproxValoresOptimos = []
    aproxTiempos = []

    #leer resultados de modelo matematico
    valoresOptimos_modelo = []
    ejecucion_modelo = [] #tiempo de ejecucion
    iteraciones_modelo = [] 

    with open('resultados_modeloMatematico.csv','r') as file:
        reader = csv.reader(file)

        next(reader) #skips the header row

        #Iteramos sobre cada fila
        for row in reader:
            valoresOptimos_modelo.append(int(row[1]))
            ejecucion_modelo.append(float(row[2]))
            iteraciones_modelo.append(int(row[3]))

    i = 0
    for key,value in datos_cargueros.items():

        pesos = datos_cargueros[key][0]
        beneficios = datos_cargueros[key][1]

        contenedores = [Contenedor(beneficios[i],pesos[i]) for i in range(0,len(beneficios))]
        start_time = timeit.default_timer()
        totalProfit,iteraciones  = carguero_problema(capacidadMax,contenedores)
        end_time = timeit.default_timer()

        execution_time =  end_time - start_time
        print(f'\nTiempo de ejecucion del algoritmo: {execution_time}s')
        print(f'\nNumero de iteraciones realizadas para seleccionar contenedores (no incluye las del sort function): {iteraciones}')
        print(f'\nFuncion objetivo: {totalProfit}\n')

        #operaciones

        nombres_cargueros.append(key)
        objetivos.append(totalProfit)
        tiempos.append(execution_time)
        try:
            aproxValoresOptimos.append(1 - round((valoresOptimos_modelo[i] - totalProfit)/valoresOptimos_modelo[i],4)) #Diferencia porcentual de optimo y el del heuristico
            aproxTiempos.append(round((execution_time)/ejecucion_modelo[i],5)) #Diferencia porcentual de tiempo de ejecucion entre modelo y heuristico
        except:
            aproxValoresOptimos.append(0)
            aproxTiempos.append(0)
        
        i += 1
        
    # Combine the values into rows and append them to the table
    for val1, val2, val3,val4,val5,val6 in zip(nombres_cargueros,valoresOptimos_modelo,objetivos,tiempos,aproxValoresOptimos,aproxTiempos):
        table_data.append([val1, val2, val3,val4,val5,val6])
            
    # Use the tabulate function to format and print the table
    table = tabulate(table_data, headers="firstrow", tablefmt="fancy_grid")
    print(table)
    
    with open('resultados.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(table_data)    

    #Promedios de valores objetivos
    prom_valObjetivos = statistics.mean(objetivos)
    prom_tiempos = statistics.mean(tiempos)
    prom_aproxValObjetivos = statistics.mean(aproxValoresOptimos)
    prom_aproxTiempos = statistics.mean(aproxTiempos)

    print(f'\nPromedio de valores objetivo del heuristico: {prom_valObjetivos}')
    print(f'\nPromedio de tiempos de ejecucion con el heuristico: {prom_tiempos}s')
    print(f'\nPromedio porcentual de aproximacion del heuristico con respecto al modelo matematico: {prom_aproxValObjetivos}')
    print(f'\nPromedio de proporcion entre el tiempo de ejecucion del heuristico con respecto al modelo: {prom_aproxTiempos}s\n')

    fig,(ax1,ax2) = plt.subplots(2)
    #grafique el promedio de los tiempos de computo para el heuristico
    x = [i for i in range(len(objetivos))]#puntos
    y1 = tiempos
    y2 = aproxTiempos
    ax1.plot(x,y1)
    ax2.plot(x,y2)

    # Set titles for each subplot
    ax1.set_title('Tiempos de ejecucion de cargueros:')
    ax2.set_title('Diferencias porcentuales de tiempo de ejecucion entre modelo y heuristico')

    # Set x and y labels for each subplot
    ax1.set_xlabel('Numero de carguero')
    ax1.set_ylabel('Tiempo (s)')
    ax2.set_xlabel('Numero de carguero')
    ax2.set_ylabel('Tiempo (s)')

    #adjust the space between subplots
    plt.subplots_adjust(wspace=0.5, hspace=0.5)

    #Graficar
    plt.show()


solucionarProblema()

