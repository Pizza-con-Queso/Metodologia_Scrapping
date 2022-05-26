import requests
import math

import time

from bs4 import BeautifulSoup

def DetectarGenero(sop):
    ini = sop.find("What is")
    fin = sop.find("best known for?")
    if (sop.find("she", ini, fin) > 0):
        return 0
    elif (sop.find("he", ini, fin) > 0):
        return 1
    else:
        return 2
        
#retornar resultado, crear funcion aplicadora

def DetectarGeneroPorPais(head, TabCien):
    Res = [0, 0, 0]
    
    for j in range(len(TabCien)):
        page = requests.get(TabCien[j], headers=head)
        soap = BeautifulSoup(page.text, 'html.parser')
        soap = str(soap)
        Res[DetectarGenero(soap)] += 1
    return Res

def DetectarGeneroPais(head):
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
    print(TabPai[Pais-1][1])

    TabCien = []
    for i in range(TabPai[Pais-1][3]):
        page = requests.get(link+'/'+TabPai[Pais-1][0]+'?page='+str(i), headers=head)
        soap = BeautifulSoup(page.text, 'html.parser')
        soap = str(soap)
        TabCien += DetectarLinksCientificos(soap)
            
    Lim = input('Ingrese el limite de resultados(0 para todos): ')
    Lim = int(Lim)
    if (Lim != 0):
        TabCien = TabCien[0:Lim]
    Res = DetectarGeneroPorPais(head, TabCien)
    print("Mujeres = ", Res[0], "\nHombres = ", Res[1], "\nNo detectado = ", Res[2])

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
        T.append( Lista[i][0:ini-1])
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
    #print(T)
    return T


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

page = requests.get('https://research.com/scientists-rankings/computer-science', headers=head)
print(page)

soup = BeautifulSoup(page.text, 'html.parser')
soup = str(soup)

DetectarGeneroPais(head)
#print(DetectarGeneroPorPais(head))
#print(DetectarLinksCientificos(soup))
#TablaPaises(soup)

def main():
    head_user = input("Ingrese su header:  ")
    
    if head_user == "t":
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    if head_user == "v":
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
    else:
        head = {'User-Agent': head_user}
    
    page = requests.get('https://research.com/scientists-rankings/computer-science', headers=head)

    if verificacion_HeadUser(page) == 1:
        menu()
    else:
        print("El head User no es correcto. Intente nuevamente")

def verificacion_HeadUser(A):
    if A == 200:
        return 1
    else:
        return 0

def menu():
    intrucciones()
    opcion = int(input("\n\nIngrese la opción que desea generar:\t"))

    while(opcion != 0):
        if opcion == 1:
            DetectarGenero(soup)
        if opcion == 2:
            TablaPaises(soup)
        if opcion == 3:
            print("Hola")
        if opcion == 4:
            print("Hola")
        if opcion == 5:
            print("Hola")
        if opcion == 6:
            print("Hola")
        else:
            print("Hola")
        
        intrucciones()

        opcion = int(input("\n\nIngrese la opción que desea generar:\t"))
        
def intrucciones():
    print("1) Identificar sexo de científicos")
    print("2) Cantidad de científicos por país")
    print("3) Cantidad de Instituciones de investigación por país")
    print("4) Coautores")
    print("5) Sub-diciplinas con más artículos publicados")
    print("6) Cantidad de Articulos citados por sub-diciplina")
    print("Salir (0)")
