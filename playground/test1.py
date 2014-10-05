# -----------
# User Instructions
# 
# Modify the valid_month() function to verify 
# whether the data a user enters is a valid 
# month. If the passed in parameter 'month' 
# is not a valid month, return None. 
# If 'month' is a valid month, then return 
# the name of the month with the first letter 
# capitalized.
#

import string
import cgi

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
def valid_month(month):
	month = month.lower()  
	month = month.title()  

	if month in months:
		return month

	else:
		return None    

def valid_day(day):
	if day and day.isdigit():
		day = int(day)
		if day > 0 and day <= 31:
			return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year > 1900 and year < 2020:
            return year

def escape_html1(s):
	for (i,o) in (("&", "&amp;"),
				  (">", "&gt;"),
				  ("<", "&lt;"),
				  ('"', "&quote;")):
		s = s.replace(i,o)
	return s	

def escape_html2(s):
	return cgi.escape(s, quote=True)



