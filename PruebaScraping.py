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
        LF += T
    print(LF)


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

page = requests.get('https://research.com/scientists-rankings/computer-science', headers=head)
print(page)

soup = BeautifulSoup(page.text, 'html.parser')
soup = str(soup)

#DetectarLinks(soup)
TablaPaises(soup)
