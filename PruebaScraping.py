import requests
import math
from bs4 import BeautifulSoup

def DetectarGenero(sop):
    ini = sop.find("The fields of study he is best known for:")
    fin = sop.find("His most cited work include:")
    print(sop.find("his", ini, fin))
    print(sop.find("her", ini, fin))

def DetectarLinks(sop):
    ini = 0
    fin = 0
    while ini != -1:
        ini = sop.find("href=\"http", ini)
        fin = sop.find("\"", ini+6)
        if ini != -1:
            print("(",ini,",",fin,")")
            print(sop[ini+6:fin])
            ini = fin

def TablaPaises(sop):
    ini = sop.find("All countries")
    fin = 0
    final = sop.find("/select", ini)
    Lista = []
    LF = []
    while fin != -1 and (ini != -1 and ini < final):
        ini = sop.find("\">", ini)
        fin = sop.find("\n</option>", ini)
        if fin != -1:
            Lista.append(str(sop[ini+3:fin]))
        ini = ini+1
        
    for i in range(len(Lista)):
        T = []
        ini = Lista[i].find("(")
        fin = Lista[i].find(")")
        print(Lista[i][0:ini])
        print(Lista[i][ini+1:fin])
        T.append( Lista[i][0:ini])
        T.append(int(Lista[i][ini+1:fin]))
        LF.append(T)
    print(LF)
    
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

#DetectarLinks(soup)
TablaPaises(soup)

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
