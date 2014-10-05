# Import Statements
from SiteHandler import * 

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect('/')
        else:
            self.redirect(users.create_login_url('/'))