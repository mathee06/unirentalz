'''
CLASS:      DataStore.py
FOR:        This class defines the Database for MacGPA. Each Class is an individual
            Table.
CREATED:    15 December 2013
MODIFIED:   15 December 2013

LOGS:
'''

# Import Statements
from google.appengine.ext import ndb

## Course Database -- User selects course from here!
class Course(ndb.Model):
    subject = ndb.StringProperty()
    code = ndb.StringProperty()
    shortSubject = ndb.StringProperty()
    name = ndb.StringProperty()
    unit = ndb.IntegerProperty()

## User Course Entry  -- Entry for User Course
class CourseEntry(ndb.Model):
    entryName = ndb.StringProperty()
    entryMark = ndb.FloatProperty()
    entryWeight = ndb.FloatProperty()
    entryTime = ndb.DateTimeProperty(auto_now_add = True)

## User Course -- Course User Has
class UserCourse(ndb.Model):
    courseInfo = ndb.StructuredProperty(Course)
    courseYear = ndb.IntegerProperty (required = True)
    courseMark = ndb.FloatProperty ()
    userID = ndb.IntegerProperty (required = True)
    semester = ndb.IntegerProperty (choices = set([1,2,3,4]))
    courseFinalGrade = ndb.StringProperty (choices = set(['0','1','2','3','4','5','6','7','8','9','10','11','12']))
    courseEntry = ndb.IntegerProperty (repeated = True)

## Course Mark -- Table for Calculating Course Average! -- To Be Used in the Future
class CourseMark(ndb.Model):
    courseInfo = ndb.StructuredProperty(Course)
    year = ndb.IntegerProperty()
    grade = ndb.FloatProperty()
    usersRegistered = ndb.IntegerProperty()

## JsonData -- Used to Store JSON Data to serve Data Quickly!
class JsonData(ndb.Model):
    json = ndb.JsonProperty()
    jsonID = ndb.StringProperty()

## User Table -- Used to Store User 
class User(ndb.Model):
    personName = ndb.StringProperty()                                   # User's Name
    firstName = ndb.StringProperty()                     # First name
    lastName = ndb.StringProperty()                      # Last name
    userName = ndb.StringProperty(required = True, indexed=True)        # User name
    email = ndb.StringProperty (required = True, indexed=True)          # User email
    passwordHash = ndb.StringProperty(required = True)                  # Password Hash
    gender = ndb.StringProperty (choices=set(["male", "female"]))       # Gender
    terms = ndb.BooleanProperty (required = True)                       # Terms agreed
    registrationDate = ndb.DateTimeProperty(auto_now_add=True)          # Registration Date
    birthday = ndb.DateProperty()                                       # Birthday
    emailConfirmHash = ndb.StringProperty ()                            # Email Confirm Hash
    passwordResetHash = ndb.StringProperty ()                           # Password Reset Hash
    emailValidated = ndb.BooleanProperty ()                             # Email Confirmed Boolean -- True if User Registers via Facebook
    userCourseKeys = ndb.IntegerProperty(repeated=True)                 # User Course Keys
    courseYears = ndb.IntegerProperty(repeated=True)                    # User Course Years
    cumulativeGPA = ndb.FloatProperty()                                 # Cumulative GPA
    convertedGPA = ndb.FloatProperty()                                  # Converted GPA
    cookie = ndb.StringProperty ()                                      # Cookie String
    userType = ndb.StringProperty (required=True, choices=set(["Administrator", "Moderator", "Regular", "Banned"]))     # User Type
    jsonData = ndb.JsonProperty()                                       # User Json Data
    fbOAuth = ndb.StringProperty()                                      # FB OAuth Token for User
    fbUserId = ndb.IntegerProperty()                                    # FB User ID
