# CUSTOM CODE IMPORTS
from SiteHandler import *
from LoginHandler import *
from LogoutHandler import * 

####### DEBUGGING: logging.info("FAILED") 
#######            python -m tabnanny main.py
#######            fuser -k 8080/tcp

MAC_ID_ERROR = False
OFFCAMPUS_URL = "https://macoffcampus.mcmaster.ca/classifieds/?cat=0&s="

def search_addr(streetNUM, streetNAME):
    #streetNUM = "27"
    #streetADDR = "Thorndale Street North"

    streetCOMPL_search = "%s+%s" %(streetNUM, streetNAME)
    streetCOMPL_find = "/%s-%s" %(streetNUM, streetNAME)

    url = OFFCAMPUS_URL + streetCOMPL_search
    logging.info("searching...." + url)
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return 

    if content:
	    #parse the HTML and find the address
	    soup = BeautifulSoup(content)
	    results = soup.find_all("div", class_="address")

	    for entry in results:
	    	match = entry.find_all(href=re.compile(streetCOMPL_find))
	    	if match:
	    		for link in match:
	    			AD_listing = link.get('href')
	    			img_urls, rentalINFO = extract_DATA(AD_listing)
	    			return (img_urls, rentalINFO)

def extract_DATA(AD_listing):
    #AD_listing = "https://macoffcampus.mcmaster.ca/classifieds/27-thorndale-st-north-wonderful-home-steps-to-mac/"

    content = None
    try:
        content = urllib2.urlopen(AD_listing).read()
    except URLError:
        return

    if content:
        #parse the HTML and extract needed data
        soup = BeautifulSoup(content)
        imgResults = soup.find_all(id="ocrc-entry-images")
        infoResults = soup.find(text="Rent Details")

        i = 0
        info_list = ["Utilities [Included in Rent]:", "Amenities:", "Network:", "Furnished:"]
        rentalINFO = {}
        img_urls = []

        #use while loop to find the rent details and add to dictionary
        while i < 4:
            infoResults = infoResults.find_next("div")
            entry =  infoResults.strong.next_element.next_element
            rentalINFO[info_list[i]] = entry
            i += 1
                
        logging.info(rentalINFO)
        
        #use for loops to add img urls to list 
        for entry in imgResults:
            match = entry.find_all(href=re.compile("uploads"))
            if match:
                for link in match:
                    img_urls.append(link.get('href'))

        return (img_urls, rentalINFO)

def rating_entityKey(name = 'default'):
    return db.entityKey.from_path('ratings', name)


class MainPage(SiteHandler):
    def get(self):
    	global MAC_ID_ERROR
        
        user = users.get_current_user()
        if user:
            if not "@mcmaster.ca" in user.nickname():
                MAC_ID_ERROR = True
                self.redirect('/logout')
        
        self.response.write("""<html>
								<head>
								</head>
								<body>""")
        if user:
            self.response.write('Hello, ' + user.nickname())
            self.response.write("""<form action="/logout?%s">
<input type="submit" value="Logout">
</form>""")
        else:
            if MAC_ID_ERROR:
                self.response.write('<p> You must login with a valid McMaster ID! </p>')
                MAC_ID_ERROR = False
            self.response.write("""<form action="/login?%s">
<input type="submit" value="Login">
</form>""")
        self.response.write("""</body>
</html>""")

        self.render("front.html")

    def post(self):
        streetADDR = self.request.get("streetADDR")
        logging.info(streetADDR)
        logging.info("INPUT SUBMITTED")

        #Check if user submitted an input
        if streetADDR: 
            logging.info("INPUT IS SOMETHING")

            #Query the DB for user requested address and check for existance in current DB
            qry = rentalPropertyDB.query(rentalPropertyDB.streetADDR == streetADDR).get()
            logging.info(type(qry))
            logging.info(qry)

            #Query DNE in current DB
            if (qry == None):
                logging.info("DOES NOT EXIST IN DB")
                tempADDR = streetADDR
                tempADDR = tempADDR.lower()
                tempADDR = tempADDR.split()

                streetNUM = tempADDR[0]
                streetNAME = tempADDR[1]

                rental = rentalPropertyDB()
                rental.streetADDR = streetADDR
                rental.streetNUM = streetNUM
                rental.streetNAME = streetNAME

                #Check if address exists on MacOffCampus 
                img_urls, rentalINFO = search_addr(streetNUM, streetNAME)
                if (type(img_urls) is list):
                    logging.info("EXISTS IN MACOFFCAMP")
                    for image in img_urls:
                    	result = urlfetch.Fetch(image)
                        if result.status_code == 200:
                        	rentalIMAGE = imageDB()
                        	logging.info("PICTURE PUT IN")
                        	rentalIMAGE.streetADDR = streetADDR
                        	rentalIMAGE.image = db.Blob(result.content)
                        	rentalIMAGE.put()
                    rental.rentalINFO = rentalINFO
                    rental.put()
                    self.redirect("/view/%s" % rental.key.id())
                else: 
                    logging.info("DOES NOT ExIST IN MACOFFCAMP")
                    self.write(streetADDR + " does not exist on MacOffCampus")
                    self.render("front.html")

            #Query E in current DB
            else:
                logging.info("QUERY EXISTS IN DB")
                self.redirect("/view/%s" % qry.key.id())

        else:
            logging.info("INPUT IS NOTHING WTF")
            self.write("Try submitting an input next time")
            self.render("front.html")

class ViewRental(SiteHandler):
    def get(self, entityKey):
        qry = rentalPropertyDB.get_by_id(int(entityKey))
        imgQry = imageDB.all()
        imgQry.filter("streetADDR =", qry.streetADDR)

        '''
        SECTION NOT USED, MAY BE USED FOR PICTURE EDITING IF NEEDED
        for picture in imgQry:
        	logging.info("YES THERE IS A FUCKING PHOTO")      	
        	img = images.Image(picture.image)
        	img.resize(width=80, height=100)
        	img.im_feeling_lucky()
        	thumbnail = img.execute_transforms(output_encoding=images.JPEG)
        	logging.info(type(p.image))
        '''
        
        self.render("viewRentalPage.html", entityKey=entityKey, qry=qry, imgQry=imgQry) 

    def post(self, entityKey):
        responsibleRating = int(self.request.get("responsibleRB"))
        leadershipRating = int(self.request.get("leadershipRB"))
        reasonableRating = int(self.request.get("reasonableRB"))
        respectfulRating = int(self.request.get("respectfulRB"))
        currentLandlord = self.request.get("currentLandlord")
        commentSubmission = self.request.get("commentSubmission")
        submitRating = self.request.get("submitRating")
        logging.info(responsibleRating)
        logging.info(leadershipRating)
        logging.info(reasonableRating)
        logging.info(respectfulRating)
        logging.info(currentLandlord)
        logging.info(commentSubmission)

        logging.info("*(*************************************************************************")
        
        if submitRating:
            logging.info("ADD RATING GOT PRESSED!")
        if (responsibleRating and leadershipRating and reasonableRating and respectfulRating and currentLandlord and commentSubmission):
            logging.info("USER SENT ALL INFO FOR RATINGS YAY")
            qry = rentalPropertyDB.get_by_id(int(entityKey))
            qry.rentalRating.append(rentalRatingDB(responsibleRating = responsibleRating,
                                                    leadershipRating = leadershipRating,
                                                    reasonableRating = reasonableRating,
                                                    respectfulRating = respectfulRating,
                                                    currentLandlord = currentLandlord,
                                                    commentSubmission = commentSubmission))
            qry.put()
            logging.info("RATING GOT PUT INTO THE DATABASE WOOOOOOO")
            self.redirect("/view/%s" % entityKey)
        else:
            logging.info("FUCK AN ERROR HAPPENED MAN")
            error = "Make sure all options are filled!"
            self.render("viewRentalPage.html", responsibleRB=responsibleRB, leadershipRB=leadershipRB, reasonableRB=reasonableRB, respectfulRB=respectfulRB, commentSubmission=commentSubmission, error=error)    
  
application = webapp2.WSGIApplication([('/', MainPage),
									   ('/login', LoginHandler),
    								   ('/logout', LogoutHandler),
                                       ('/view/([^/]+)', ViewRental),
                                       ], debug=True)


'''
http://themeforest.net/search?utf8=%E2%9C%93&category=site-templates&term=bootstrap+3
Shit to Do:
- error handling for no input (Uncaught TypeError: Cannot read property '0' of undefined)
- ensure search input is not just a street name 
- listing page 
    - code to dump needed data on page
- clean up files 
- re-direct if page does not exist
- avoiding errors in empty addratings form
'''


