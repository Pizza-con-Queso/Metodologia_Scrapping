import requests
import math

import time

from colorama import init
from termcolor import colored

from bs4 import BeautifulSoup

import sys
import operator

import os

init()

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
        file.write("\n")
    show(0)
    for i, item in enumerate(it):
        yield i
        show(i+1)
        file.write("\n")
    file.flush()

def PrintGeneroPais(Res):
    print(colored("Mujeres = ", 'blue'), Res[0], colored("\nHombres = ", 'magenta'), Res[1], colored("\nNo detectado = ", 'yellow'), Res[2])

def PrintArticulosPais(Res):
    print ("{:<40} {:<7}".format('Nombre','Cantidad articulos'))
    for i in Res:
        print ("{:<40} {:<7}".format(colored(i[0], 'green'), colored(i[1], 'cyan')))

def PrintArticulosCitas(Res):
    print ("{:<70} {:<10}".format('Nombre articulo','Cantidad citas'))
    for i in Res:
        print ("{:<70} {:<10}".format(colored(i[0], 'green'), colored(i[1], 'cyan')))
        
def PrintInstituciones(Res):
    print ("{:<50} {:<10}".format('Nombre institucion','Cantidad cientificos'))
    for i in Res:
        print ("{:<50} {:<10}".format(colored(i[0], 'green'), colored(i[1], 'cyan')))

def PrintCoAutores(Res):
    print ("{:<50} {:<10}".format('Nombre','Cantidad co-autorias'))
    for i in Res:
        print ("{:<50} {:<10}".format(colored(i[0], 'green'), colored(i[1], 'cyan')))
        
def DetectarPorPais(head, fun_Res, fun_Print):
    link = 'https://research.com/scientists-rankings/computer-science'
    page = requests.get(link, headers=head)
    soap = BeautifulSoup(page.text, 'html.parser')
    soap = str(soap)
    
    TabPai = TablaPaises(soap)
    print("Listado paises:")
    for i in range(len(TabPai)):
        print('\t',i+1,'-', TabPai[i][1])
        
    Pais = input('Ingrese el numero del pais a buscar: ')
    Pais = int(Pais)
    print(TabPai[Pais-1][1], " seleccionado")

    Lim = input('Ingrese el limite de resultados(maximo '+ str(TabPai[Pais-1][2])+'): ')
    Lim = int(Lim)
    
    TabCien = []
    for i in range(math.ceil(Lim/100)):
        page = requests.get(link+'/'+TabPai[Pais-1][0]+'?page='+str(i+1), headers=head)
        soap = BeautifulSoup(page.text, 'html.parser')
        soap = str(soap)
        TabCien += DetectarLinksCientificos(soap)
            
    TabCien = TabCien[0:Lim]
    
    Res = fun_Res(head, TabCien)

    fun_Print(Res)

def ObtenerCantidadDeArticulos(sop):
    div = sop.split('\n')
    if sop.find(',') != -1:
        return int(sop[0])*1000 + int(sop[2::])
    else:
        return int(sop)

def ObtenerSubdiciplinas(sop, pos):
    t = sop[pos+2]
    p1 = t.find("(")
    a = [t[4:p1-1], float(t[p1+1:t.find("%")])]
    t = sop[pos+3]
    p1 = t.find("(")
    b = [t[4:p1-1], float(t[p1+1:t.find("%")])]
    t = sop[pos+4]
    p1 = t.find("(")
    c = [t[4:p1-1], float(t[p1+1:t.find("%")])]
    return [a, b, c]

def BuscarSeccion(sop, text):
    for i in range(len(sop)):
        if sop[i].find(text) != -1:
            return i
    return -1

def AgregarSubdiciplina(LT, N):
    for i in LT:
        if i[0] == N[0]:
            i[1] += N[2]
            return
    LT.append([N[0], N[2]])

def DetectarCantidadArticulosPorPais(head, TabCien):
    Res = []
    clear()
    for j in progressbar(range(len(TabCien)), "Calculando: ", 40):
        page = requests.get(TabCien[j], headers=head)
        soap = page.text.split('\n')
        cant = ObtenerCantidadDeArticulos(soap[306])
        pos = BuscarSeccion(soap, "He most often published in these fields")
        if pos != -1:
            subs = []
            subs = ObtenerSubdiciplinas(soap, pos)
            for h in range(0,3):
                subs[h].append(math.floor((subs[h][1]/100)*cant))
                AgregarSubdiciplina(Res, subs[h])
        clear()
    Res = sorted(Res, key=operator.itemgetter(1), reverse = True)
    return Res
#Retorna tabla de articulos [[Nombre, cantidad articulos]...]

def ObtenerTablaArticulosCitas(head, TabCien):
    Res = []
    clear()
    for j in progressbar(range(len(TabCien)), "Calculando: ", 40):
        page = requests.get(TabCien[j], headers=head)
        soap = page.text.split('\n')
        pos = BuscarSeccion(soap, "Top Publications")
        soap = soap[pos+1:]
        pos = BuscarSeccion(soap, "Top Publications")
        if pos != -1:
            pos += 3
            for i in range(10):
                ini = soap[pos+1].find('>')
                fin = soap[pos+1][2:].find('<')
                tmp = [soap[pos+1][ini+1:fin+2], int(soap[pos+8][:soap[pos+8].find(' ')])]
                Res.append(tmp)
                pos += 10
        clear()
    Res = sorted(Res, key=operator.itemgetter(1), reverse = True)
    return Res
#Retorna tabla de subdiciplinas [[Nombre, cantidad articulos]...]

def ObtenerInstituciones(head, TabCien):
    Res = []
    clear()
    for j in progressbar(range(len(TabCien)), "Calculando: ", 40):
        page = requests.get(TabCien[j], headers=head)
        soap = page.text.split('\n')
        AgregarSubdiciplina(Res, [soap[269], None, 1])
        clear()
    Res = sorted(Res, key=operator.itemgetter(1), reverse = True)
    return Res
#Retorna tabla de instituciones [[Nombre, cantidad cientificos]...]

def ObtenerTablaCoAutores(head, TabCien):
    Res = []
    clear()
    for j in progressbar(range(len(TabCien)), "Calculando: ", 40):
        page = requests.get(TabCien[j], headers=head)
        soap = page.text.split('\n')
        pos = BuscarSeccion(soap, "Co-Authors")
        if pos != -1:
            pos += 1
            for i in range(10):
                AgregarSubdiciplina(Res, [soap[pos+4], None, 1])
                pos += 9
        clear()
    Res = sorted(Res, key=operator.itemgetter(1), reverse = True)
    return Res
#Retorna tabla de coautores [[Nombre, cantidad repeticiones]...]

def DetectarGenero(sop):
    ini = sop.find("What is")
    fin = sop.find("best known for?")
    if (sop.find("she", ini, fin) > 0):
        return 0
    elif (sop.find("he", ini, fin) > 0):
        return 1
    else:
        return 2

def DetectarGeneroPorPais(head, TabCien):
    Res = [0, 0, 0]
    clear()
    for j in progressbar(range(len(TabCien)), "Calculando: ", 40):
        page = requests.get(TabCien[j], headers=head)
        soap = page.text
        Res[DetectarGenero(soap)] += 1
        clear()
    return Res
#Retorna tabla de generos [M, H, N]

def TablaPaises(sop):
    ini = sop.find("All countries")
    fin = 0
    final = sop.find("/select", ini)
    Lista = []
    L2 = []
    LF = []
    while fin != -1 and (ini != -1 and ini < final):
        ini = sop.find("\">", ini)
        fin = sop.find("\n</option>", ini)
        L2.append(sop[ini-2: ini])
        if fin != -1:
            Lista.append(str(sop[ini+3:fin]))
        ini = ini+1
    for i in range(len(Lista)):
        T = []
        ini = Lista[i].find("(")
        fin = Lista[i].find(")")
        T.append(L2[i])
        T.append(Lista[i][0:ini-1])
        T.append(int(Lista[i][ini+1:fin]))
        T.append(math.ceil(int(Lista[i][ini+1:fin])/100))
        LF.append(T)
    return LF
#Retorna tabla de paises [[a, p, c, f], ...]
#   a = acronimo pais:          string
#   p = nombre pais:            string
#   c = cantidad cientificos:   int
#   f = cantidad de paginas:    int
    
def DetectarLinksCientificos(sop):
    ini = 0
    fin = 0
    T = []
    while ini != -1:
        ini = sop.find("href=\"https://research.com/u/", ini)
        fin = sop.find("\"", ini+6)
        if ini != -1:
            T.append(sop[ini+6:fin]+"/") 
            ini = fin
    return T

def main():
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    
    page = requests.get('https://research.com/scientists-rankings/computer-science', headers=head)

    if verificacion_HeadUser(page.status_code) == 1:
        menu(head)
    else:
        print("El head User no es correcto. Intente nuevamente")

def verificacion_HeadUser(A):
    if A >= 200 and A < 300:
        return 1
    else:
        return 0

def menu(head):
    opcion = 1
    while(opcion > 0 and opcion <= 5):
        intrucciones()
        opcion = int(input("\n\nIngrese la opción que desea generar:\t"))
        if opcion == 1:
            DetectarPorPais(head, DetectarGeneroPorPais, PrintGeneroPais)
        elif opcion == 2:
            DetectarPorPais(head, ObtenerInstituciones, PrintInstituciones)
        elif opcion == 3:
            DetectarPorPais(head, ObtenerTablaCoAutores, PrintCoAutores)
        elif opcion == 4:
            DetectarPorPais(head, DetectarCantidadArticulosPorPais, PrintArticulosPais)
        elif opcion == 5:
            DetectarPorPais(head, ObtenerTablaArticulosCitas, PrintArticulosCitas)
        else:
            print("Saliendo")
        
def intrucciones():
    print("\n\n")
    print("1) Identificar sexo de científicos de un pais")
    print("2) Cantidad de Instituciones de investigación por país")
    print("3) Coautores")
    print("4) Sub-diciplinas con más artículos publicados")
    print("5) Cantidad de Articulos citados por sub-diciplina")
    print("Salir (0)")


main()
