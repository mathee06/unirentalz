"""
CLASS:      ContactHandler.py
FOR:        This Class is responsible for handling Contact Us Page.
CREATED:    21 December 2013
MODIFIED:   21 December 2013

LOGS:
"""

# Import Statements
from BaseHandler import *
import Cookies
import EmailHandler

# Terms Class
class ContactHandler(BaseHandler):
    def get(self):
        loggedin = Cookies.validUserCookie(self.request.cookies.get('User'))

        if loggedin:
            self.render("contact.html")
        else:
            self.render('contactAnon.html')

    def post(self):
        formType = self.request.get('contactForm')

        if formType == "Anonymous":
            email = self.request.get('email')
            subject = self.request.get('subject')
            message = self.request.get('message')
            ipAddress = self.request.remote_addr

            EmailHandler.contactUsAnon(email, subject, message, ipAddress)
            self.render('contactAnonSuccess.html')

        elif formType == "LoggedIn":
            subject = self.request.get('subject')
            message = self.request.get('message')
            ipAddress = self.request.remote_addr

            user = Cookies.userFromCookie(self.request.cookies.get('User'))

            if user:
                EmailHandler.contactUs(user.personName, user.email, user.key.id(), subject, message, ipAddress)
                self.render('contactSuccess.html')

            else:
                logging.critical("ERROR: Someone's Trying Something Funny w/ Contact Form")
                self.redirect('/contact')
