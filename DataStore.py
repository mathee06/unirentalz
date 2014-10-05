# Import Statements
from google.appengine.ext import ndb
from google.appengine.ext import db

# rentalPropertyDB -- Used to store all information pertaining to the rental 
class rentalPropertyDB(ndb.Model):
    streetADDR = ndb.StringProperty(required=True)
    streetNUM = ndb.StringProperty(required=True)
    streetNAME = ndb.StringProperty(required=True)
    rentalINFO = ndb.JsonProperty(default=None)
    rentalRating = ndb.StructuredProperty(rentalRatingDB, repeated=True)

# imageDB -- Used to store all images for each rental property
class imageDB(db.Model):
	streetADDR = db.StringProperty()
	image = db.BlobProperty()

# rentalRatingDB -- Stores all rating info for each rental property
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

