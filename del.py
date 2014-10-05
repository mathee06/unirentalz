'''
FILE:       main.py
PURPOSE:    Main class -- maps the controller to the URL 
MODIFIED:   6 March 2014
AUTHOR:     Mathee Sivananthan
'''
from google.appengine.api import urlfetch
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api.images import get_serving_url

# CUSTOM CODE IMPORTS
from SiteHandler import *
from LoginHandler import *

####### DEBUGGING: logging.info("FAILED") 
#######            python -m tabnanny main.py
#######            fuser -k 8080/tcp

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

class rentalRatingDB(ndb.Model): 
    leadershipRating = ndb.IntegerProperty(required=True)
    responsibleRating = ndb.IntegerProperty(required=True)
    respectfulRating = ndb.IntegerProperty(required=True)
    reasonableRating = ndb.IntegerProperty(required=True)
    commentSubmission = ndb.StringProperty(required=True)
    currentLandlord = ndb.StringProperty(required=True)
    dateCreated = ndb.DateTimeProperty(auto_now_add = True)

    def render(self):
    	return render_str("viewRentalPage.html", rating=self)

class rentalPropertyDB(ndb.Model):
    streetADDR = ndb.StringProperty(required=True)
    streetNUM = ndb.StringProperty(required=True)
    streetNAME = ndb.StringProperty(required=True)
    image = ndb.BlobProperty(default=None) 
    rentalCoords = ndb.GeoPtProperty(default=None)
    rentalINFO = ndb.JsonProperty(default=None)
    rentalRating = ndb.StructuredProperty(rentalRatingDB, repeated=True)

class MainPage(SiteHandler, blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
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
                logging.info("FIND ME ALLLLL THE PICTURES!")
                logging.info(img_urls)
                if (type(img_urls) is list):
                    logging.info("EXISTS IN MACOFFCAMP")
                    for image in img_urls:
                    	logging.info(image)
                    	upload_files = self.get_upload(image)
                    	logging.info(upload_files)
                    	blob_info = upload_files[0]
                    	logging.info(blob_info)
                    	rental.image_name = blob_info.filename
                    	rental.image_url = get_serving_url(blob_info.key())
                    	#urlfetch.set_default_fetch_deadline(60)
                    	#rental.image = urlfetch.Fetch(image).content
                    rental.rentalINFO = rentalINFO
                    rental.put()
                    self.redirect("/view/%s" % rental.key.id())
                else: 
                    logging.info("DOES NOT EXIST IN MACOFFCAMP")
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
        self.render("viewRentalPage.html", entityKey=entityKey, qry=qry) 

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
                                       ('/view/([^/]+)', ViewRental),
                                       ('/login', LoginHandler),
                                       ('/access', AccessHandler),
                                       ('/code', CodeHandler)
                                       ], debug=True)


'''
http://themeforest.net/search?utf8=%E2%9C%93&category=site-templates&term=bootstrap+3
Shit to Do:
- force user to select from suggestion
- error handling for no input (Uncaught TypeError: Cannot read property '0' of undefined)
- ensure search input is not just a street name 
- listing page 
    - code to dump needed data on page
- clean up files 
- login system (tv)
- beautify the listing page (tv)
- re-direct if page does not exist
- avoiding errors in empty addratings form
'''


