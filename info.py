from bs4 import BeautifulSoup
import re
import urllib2 

AD_listing = "https://macoffcampus.mcmaster.ca/classifieds/27-thorndale-st-n-wonderful-home-steps-to-mac/"

content = None
try:
	content = urllib2.urlopen(AD_listing).read()
except URLError:
	None

if content:
	soup = BeautifulSoup(content)
	infoResults = soup.find(text="Rent Details")

	i = 0 
	info_list = ["Utilities [Included in Rent]:", "Amenities:", "Network", "Furnished"]
	rentalINFO = {}
	
	#use while loop to find the rent details and add to dictionary
	while i < 4:
		infoResults = infoResults.find_next("div")
		entry =  infoResults.strong.next_element.next_element
		rentalINFO[info_list[i]] = entry
		i += 1

	print rentalINFO

	 


