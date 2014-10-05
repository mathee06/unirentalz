#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Import Statements -- Builtin Libraries

'''
CLASS:      main.py
FOR:        The main class for MacGPA. This maps the controller to the URL
CREATED:    15 December 2013
MODIFIED:   15 December 2013

LOGS:       Removed useless imports: re, hashlib, string, time
'''

## Custom Code Imports
from BaseHandler import *                       ## Base Handler
from HomePageHandler import *                   ## Home Page --- /
from RegisterationHandler import *              ## Reigsteration Page --- /register
from TermsHandler import *			## Terms Page --- /terms
from ContactHandler import *		        ## Contact Us --- /contact
from LogoutHandler import *			## Logout --- /logout
from AutoAddHandler import *		        ## AutoAdd --- /autoadd
from GradesHandler import *			## Grades --- /grades
from EmailValidationHandler import *            ## Email Validation --- /confirm
from API_DropdownCourseList import *            ## Course Lsit --- /API/dropdownCourseList
from API_AddCourseFromDropdown import *         ## Add New Course Dropdown --- /API/addDropdownCourse
from API_MyCourses import *                     ## Fetch My Course List --- /API/myCourses
from API_AddNewCourseEntry import *             ## Add New Course Entry --- /API/addNewCourseEntry
from DialogTemplateHandler import DeleteEntryHandler        ## Delete Entry Confirmation Template --- /dialogTemplate/deleteEntryConfirm
from DialogTemplateHandler import DeleteCourseHandler       ## Delete Course Confirmation Template --- /dialogTemplate/deleteCourseConfirm
from DialogTemplateHandler import EditEntryHandler          ## Edit Course Entry Template --- /dialogTemplate/editCourseEntry
from API_DeleteEntry import *                   ## Delete Course Entry --- /API/deleteEntry
from API_DeleteCourse import *                  ## Delete Course --- /API/deleteCourse
from API_UpdateFinalGrade import *              ## Update Final Course Grade --- /API/updateFinalGrade
from API_EditCourseEntry import *               ## Edit Course Entry --- /API/editCourseEntry
from ForgotPasswordHandler import *             ## Forgot Password --- /forgotpassword
from ForgotUsernameHandler import *             ## Forgot Username --- /forgotusername
from ResetPasswordHandler import *              ## Reset Password --- /resetpassword
from SettingsHandler import *                   ## Settings --- /settings

## Main Display When you visit Site
class MainHandler(BaseHandler):
    def get(self):
        self.render ("homepage.html")

# URL / Class Mapping
app = webapp2.WSGIApplication([
    ('/', HomePageHandler),
    ('/register', RegisterationHandler),
    ('/terms', TermsHandler),
    ('/contact', ContactHandler),
    ('/logout', LogoutHandler),
    ('/autoadd', AutoAddHandler),
    ('/grades', GradesHandler),
    ('/confirm', EmailValidationHandler),
    ('/API/dropdownCourseList', API_DropdownCourseList),
    ('/API/addDropdownCourse', API_AddCourseFromDropdown),
    ('/API/myCourses', API_MyCourses),
    ('/API/addNewCourseEntry', API_AddNewCourseEntry),
    ('/dialogTemplate/deleteEntryConfirm', DeleteEntryHandler),
    ('/API/deleteEntry', API_DeleteEntry),
    ('/dialogTemplate/deleteCourseConfirm', DeleteCourseHandler),
    ('/API/deleteCourse', API_DeleteCourse),
    ('/API/updateFinalGrade', API_UpdateFinalGrade),
    ('/dialogTemplate/editCourseEntry', EditEntryHandler),
    ('/API/editCourseEntry', API_EditCourseEntry),
    ('/forgotpassword', ForgotPasswordHandler),
    ('/forgotusername', ForgotUsernameHandler),
    ('/resetpassword', ResetPasswordHandler),
    ('/settings', SettingsHandler)
], debug=True)
