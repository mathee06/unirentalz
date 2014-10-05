import os
import sys
import re
import webapp2
import jinja2
import time
import urllib2
from xml.dom import minidom

from string import letters

from google.appengine.ext import db 

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

art_key = db.Key.from_path('ASCIIChan', 'arts')

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    #ip = "4.2.2.2"
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return 

    if content:
        #parse the xml and find the coordinates
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmap_img(points):
    markers = '&'.join('markers=%s,%s' %(a.lat, a.lon) for a in points)
    return GMAPS_URL + markers

#required=True ensures property is required in the database
#auto_now_add=True ensures current date and time is automatically added
class ArtSubmission(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM ArtSubmission WHERE ANCESTOR IS :1 ORDER BY created desc LIMIT 10", art_key)
        
        #prevents the running of multiple queries
        arts = list(arts)

        #find which arts have coords
        points = filter(None, (a.coords for a in arts))
        #self.write(repr(points))       ---USED FOR DEBUGGING        

        #if we have an artsubmissions have coords, make an image url
        img_url = None
        if points:
            img_url = gmap_img(points)

        #arts from GQL query gets passed to front.html's for loop  
        self.render("front.html", title=title, art=art, error=error, arts=arts, img_url = img_url)

    def get(self):
        #self.write(self.request.remote_addr)       -- USED FOR DEBUGGING
        #self.write(repr(get_coords(self.request.remote_addr)))  #repr puts quotes around tags
        return self.render_front()       #displays blank template "front.html" (calls render_front func)

    def post(self):
        title = self.request.get("title")   #saves title submission
        art = self.request.get("art")       #saves art submission

        if title and art:
            a = ArtSubmission(parent = art_key, title = title, art = art)
            #lookup the user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)
            #if we have coordinates, add them to the Art
            if coords:
                a.coords = coords
            a.put()         #stores new art instance in database
            time.sleep(1)
            self.redirect("/")
        else:
            error = "We need both a title and some artwork!"
            self.render_front(title, art, error)    #ensures title,art,error gets sent upon error

application = webapp2.WSGIApplication([('/', MainPage)], debug=True)
