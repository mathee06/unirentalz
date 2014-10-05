'''
CLASS:      HomePageHandler.py
FOR:        Handles the Homepage for MacGPA. Includes Login. 
CREATED:    15 December 2013
MODIFIED:   20 December 2013

LOGS:
20 December 2013
- Added Full Functionality to Home / Login Page
'''

## Import Statements
from BaseHandler import *
import HTMLMsg
import bcrypt

class HomePageHandler (BaseHandler):
    # Handles Visit to Website!
    # Add part if cookie is set ... redirect to /grades
    def get (self):
        # Checking if User is Logged in
        loggedin = Cookies.validUserCookie(self.request.cookies.get('User'))

        # Redirect to Grade if User is Logged In
        if loggedin:
            self.redirect('/grades')

        # Render Homepage if user is not logged in
        else:
            self.render("homepage.html",
                errorMsg="")

    # Handles the Login Form to Website
    def post (self):
        # Getting Form Data
        userName = self.request.get("username")
        password = self.request.get("password")
        remember = self.request.get("remember")

        # Remember Boolean
        if remember == 'on':
            remember = True
        else:
            remember = False

        # Check to ensure userName and Password are not Null
        userNameNotNull, passwordNotNull = True, True

        if len(userName) <= 0:
            userNameNotNull = False
            # Rendering With Error Message
            self.render ("homepage.html",
                errorMsg=HTMLMsg.createErrorMsg("<strong>Missing Username:</strong> Enter and try again!"))
        
        elif len(password) <= 0:
            passwordNotNull = False
            # Re-render with error mesage
            self.render("homepage.html",
                errorMsg=HTMLMsg.createErrorMsg("<strong>Missing Password:</strong> Enter and try again!"))

        # Log in the User
        if userNameNotNull and passwordNotNull:
            try:
                # Find userName in DataStore
                user = ndb.gql("select * from User where userName=:1", userName).get()
                if user:
                    # Validate Login
                    passwordEntered = bcrypt.hashpw(password, user.passwordHash)

                    # Valid Login
                    if (passwordEntered == user.passwordHash) and user.emailValidated:
                        eval(Cookies.setUserCookie(user.key.id(), remember))
                        self.redirect('/grades')
                    
                    # User Email Not Yet Validated
                    elif user.emailValidated == False:
                        self.render("homepage.html",
                            errorMsg=HTMLMsg.createErrorMsg("<strong>Email Verification:</strong> Verify your email by clicking the link you got in an email!"))

                    # Invalid Login
                    else:
                        self.render("homepage.html",
                            errorMsg=HTMLMsg.createErrorMsg("<strong>Invalid Login:</strong> Please try again!"))

                # Invalid Username
                else:
                    self.render("homepage.html",
                        errorMsg=HTMLMsg.createErrorMsg("<strong>Invalid Login:</strong> Please try again!"))

            except:
                logging.info("EXCEPTION")
                self.render("homepage.html",
                    errorMsg=HTMLMsg.createErrorMsg("<strong>Invalid Login:</strong> Please try again!"))