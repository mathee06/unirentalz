'''
CLASS:      BaseHandler.py
FOR:        This class defines the Base for rendering HTML files. 
CREATED:    15 December 2013
MODIFIED:   15 December 2013

LOGS:
'''

# Import Statements
import jinja2
import webapp2
import os
import logging
from DataStore import *
import Cookies
import json

#Directory for Templates
template_dir = os.path.join(os.path.dirname(__file__), "HTML")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

#Setting Universal Logging Level To INFO
logging.getLogger().setLevel(logging.INFO)

# Render Function
def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

# BaseHandler Class
class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
