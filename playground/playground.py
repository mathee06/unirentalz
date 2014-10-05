

content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
results = soup.find_all("div", class_="address")

for entry in results:
...     x = entry.find_all(href=re.compile("/9-thorndale"))
...     if x:
...             for link in x:
...                     print(link.get('href'))


#####
content = urllib2.urlopen(url).read()
soup = BeautifulSoup(content)
results = soup.find_all(id="ocrc-entry-images")

>>> for entry in results:
...     x = entry.find_all(href=re.compile("uploads"))
...     if x:
...             for link in x:
...                     print(link.get('href'))
