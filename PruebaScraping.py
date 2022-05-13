import requests
from bs4 import BeautifulSoup


head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

page = requests.get('https://research.com/u/anil-k-jain/', headers=head)
print(page)

soup = BeautifulSoup(page.text, 'html.parser')
soup = str(soup)

ini = soup.find("The fields of study he is best known for:")
fin = soup.find("His most cited work include:")

print(soup.find("his", ini, fin))
print(soup.find("her", ini, fin))
