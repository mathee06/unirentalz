'''
CLASS:      LogoutHandler.py
FOR:        This Class is responsible for handling Contact Us Page.
CREATED:    24 December 2013
MODIFIED:   24 December 2013

LOGS:
'''

# Import Statements
from BaseHandler import *

# Terms Class
class LogoutHandler(BaseHandler):
    def get(self):
        eval(Cookies.removeUserCookie())
        self.redirect('/')