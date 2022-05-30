import requests
import math

import time

from bs4 import BeautifulSoup

import sys
import operator

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

    for j in progressbar(range(len(TabCien)), "Calculando: ", 40):
        page = requests.get(TabCien[j], headers=head)
        soap = page.text.split('\n')
        cant = ObtenerCantidadDeArticulos(soap[306])
        pos = BuscarSeccion(soap, "He most often published in these fields")
        if pos != -1:
            subs = []
            subs = ObtenerSubdiciplinas(soap, pos)
            subs[0].append(math.floor((subs[0][1]/100)*cant))
            subs[1].append(math.floor((subs[1][1]/100)*cant))
            subs[2].append(math.floor((subs[2][1]/100)*cant))
            for h in range(0,3):
                AgregarSubdiciplina(Res, subs[h])

    Res = sorted(Res, key=operator.itemgetter(1), reverse = True)
    return Res
#Retorna tabla de subdiciplinas [[Nombre, cantidad articulos]...]

def DetectarCantidadArticulosPais(head):
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
    
    Res = DetectarCantidadArticulosPorPais(head, TabCien)


    print ("{:<40} {:<7}".format('Nombre','Cantidad articulos'))

    for i in Res:
        print ("{:<40} {:<7}".format(i[0], i[1]))






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
    
    for j in range(len(TabCien)):
        t1 = time.time()
        page = requests.get(TabCien[j], headers=head)
        t2 = time.time()
        print("Get = ", t2-t1)
        #t1 = time.time()
        #soap = BeautifulSoup(page.text, 'html.parser')
        #t2 = time.time()
        #print("soup = ", t2-t1)
        #soap = str(soap)
        soap = page.text
        Res[DetectarGenero(soap)] += 1
    return Res
#Retorna tabla de generos [M, H, N]

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
    print(TabPai[Pais-1][1], " seleccionado")

    Lim = input('Ingrese el limite de resultados(maximo '+ str(TabPai[Pais-1][2])+'): ')
    Lim = int(Lim)
    
    TabCien = []
    for i in range(math.ceil(Lim/100)):
        print(i+1)
        page = requests.get(link+'/'+TabPai[Pais-1][0]+'?page='+str(i+1), headers=head)
        soap = BeautifulSoup(page.text, 'html.parser')
        soap = str(soap)
        TabCien += DetectarLinksCientificos(soap)
            
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

def main():
    head_user = input("Ingrese su header:  ")
    
    if head_user == 't':
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    elif head_user == 'v':
        head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'}
    else:
        head = {'User-Agent': head_user}
    
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
    while(opcion > 0 and opcion <= 6):
        intrucciones()
        opcion = int(input("\n\nIngrese la opción que desea generar:\t"))
        if opcion == 1:
            DetectarGeneroPais(head)
        elif opcion == 2:
            print("Hola")
            TablaPaises(soup)
        elif opcion == 3:
            print("Hola")
        elif opcion == 4:
            print("Hola")
        elif opcion == 5:
            DetectarCantidadArticulosPais(head)
        elif opcion == 6:
            print("Hola")
        else:
            print("Saliendo")
        
def intrucciones():
    print("\n\n")
    print("1) Identificar sexo de científicos de un pais")
    print("2) Cantidad de científicos por país")
    print("3) Cantidad de Instituciones de investigación por país")
    print("4) Coautores")
    print("5) Sub-diciplinas con más artículos publicados")
    print("6) Cantidad de Articulos citados por sub-diciplina")
    print("Salir (0)")


main()
