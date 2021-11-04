import sys
import argparse
import numpy as np

def media_geometrica(lista):
    return (np.prod(lista)) ** (1/len(lista))

def media_ponderada(lista, pesos):
    return (sum([x * y for x, y in zip(lista, pesos)])) / sum(pesos)

def argumentos():
    parser = argparse.ArgumentParser(usage='%(prog)s [opciones] archivo',
                                     description='Calcula cual es la computadora con mejor desempeño.')

    medias = parser.add_mutually_exclusive_group(required=True)
    salida = parser.add_mutually_exclusive_group(required=True)

    medias.add_argument('-g', '--geometrica',
                        action='store_true',
                        help='Procesa los datos con la media geometrica')
    medias.add_argument('-p', '--ponderada',
                        action='store_true',
                        help='Procesa los datos con la media ponderada')

    salida.add_argument('-r', '--rendimiento',
                        action='store_true',
                        help='Se usa si los valores del archivo miden el rendimiento')
    salida.add_argument('-t', '--tiempo',
                        action='store_true',
                        help='Se usa si los valores del archivo miden el tiempo de respuesta')

    parser.add_argument('-R', '--Resultados',
                        action='store_true',
                        help='Muestra los resultados de cada computadora')

    parser.add_argument('archivo', type=argparse.FileType('r'))

    return parser.parse_args()

def error(s):
    print(s)
    exit(1)

def main():
    args = argumentos()

    with args.archivo as file:
        linea = file.readline().rstrip()

        if not linea:
            error("Error: Inserta el número de computadoras y el número de resultados")

        try:
            tupla = tuple(map(int, linea.split(" ")))
        except ValueError:
            error("Error: El archivo solo debe de contener números")

        if len(tupla) != 2:
            error("Error: Número de computadoras y resultados incorrectos")

        nc, np = tupla
        l = file.read().splitlines()
        banderas = vars(args)

        if banderas['ponderada']:
            if nc == len(l):
                error("Error: Faltan los pesos")
            elif nc + 1 != len(l):
                error("Error: Número de datos incorrectos")
        if banderas['geometrica']:
            if nc + 1 == len(l):
                error("Error: Para calcular los datos con los pesos usa la bandera -p")
            elif nc != len(l):
                error("Error: Número de datos incorrectos")

        l2 = []
        for word in l:
            l = word.strip().split(" ")

            if len(l) != np:
                error("Error: Faltan pruebas en el archivo")

            try:
                word = list(map(float, l))
            except ValueError:
                error("Error: El archivo solo debe de contener números")

            l2.append(word)

        diccionario = {}
        if banderas['ponderada']:
            pesos, *pruebas = l2
            for i, val in enumerate(pruebas):
                diccionario[f"PC{i}"] = media_ponderada(val, pesos)

        if banderas['geometrica']:
            normal = l2[0]
            for i, val in enumerate(l2):
                val = [x / y for x, y in zip(val, normal)]
                diccionario[f"PC{i}"] = media_geometrica(val)

        if banderas['Resultados']:
            print(diccionario)

        if banderas['tiempo']:
            print(min(diccionario, key=diccionario.get))
            exit(0)

        if banderas['rendimiento']:
            print(max(diccionario, key=diccionario.get))
            exit(0)

main()
