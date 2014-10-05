import webapp2
import test1

form="""
<form method="post"> 
	What is your birthday?
	<br>
	<label>Month <input type"text" name="month" value="%(month)s"></label>
	<label>Day <input type"text" name="day" value="%(day)s"></label>
	<label>Year <input type"text" name="year" value="%(year)s"></label>
	<div style="color:red">%(error)s</div>
	<br>
	<br>
	<input type="submit"> 
</form>
"""

class MainPage(webapp2.RequestHandler):
	def write_form(self, error="", month="", day="", year=""):
		self.response.write(form %{"error":error,
									"month": test1.escape_html2(month),
									"day": test1.escape_html2(day),
									"year": test1.escape_html2(year)})

	def get(self):
		self.write_form()

	def post(self):
		user_month = self.request.get('month')
		user_day = self.request.get('day')
		user_year = self.request.get('year')

		month = test1.valid_month(user_month)
		day = test1.valid_day(user_day)
		year = test1.valid_year(user_year)

		if not (month and day and year):
			self.write_form("That doesn't look valid to me.",
							user_month, user_day, user_year)
		else:
			self.redirect("/thanks")

class ThanksHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write("Thanks! Valid Entry")

application = webapp2.WSGIApplication([('/', MainPage), ('/thanks', ThanksHandler)],debug=True)


"""
<form action="https://macoffcampus.mcmaster.ca/classifieds/"> <!--inputs search query to site-->
	<input type="hidden" name="cat" value="0"/>
	<input name="s"> <!--name for search parameter-->
	<input type="submit"> <!--creates a submit button-->
</form>

class TestHandler(webapp2.RequestHandler):
	def post(self):
		#q = self.request.get("q")
		#self.response.write(q)
		#cat = self.request.get("cat")
		#self.response.write(cat)

		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(self.request)

		application = webapp2.WSGIApplication([('/', MainPage),
									   ('/testform', TestHandler)], 
									debug=True)


"""