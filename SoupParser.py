from bs4 import BeautifulSoup
import csv
import requests

with open('SoupData.csv', 'wb') as csvfile:
		soupwriter = csv.writer(csvfile, delimiter=',',
								quotechar= '|', quoting=csv.QUOTE_MINIMAL)
		soupwriter.writerow('Hello World')
url = raw_input("Enter a website to extract the URL's from: ")

r  = requests.get("http://" +url)

data = r.text

soup = BeautifulSoup(data)

for link in soup.find_all('a'):
    print(link.get('href'))
	
	
raw_input("Are you done yet?: ")