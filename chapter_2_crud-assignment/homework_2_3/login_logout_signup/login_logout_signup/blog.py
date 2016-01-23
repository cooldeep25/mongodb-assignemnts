
#
# Copyright (c) 2008 - 2013 10gen, Inc. <http://10gen.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#



import pymongo
import sessionDAO
import userDAO
import bottle
import cgi
import re



__author__ = 'aje'


# General Discussion on structure. This program implements a blog. This file is the best place to start to get
# to know the code. In this file, which is the controller, we define a bunch of HTTP routes that are handled
# by functions. The basic way that this magic occurs is through the decorator design pattern. Decorators
# allow you to modify a function, adding code to be executed before and after the function. As a side effect
# the bottle.py decorators also put each callback into a route table.

# These are the routes that the blog must handle. They are decorated using bottle.py

# This route is the main page of the blog
@bottle.route('/')
def blog_index():

	print("\n Under Route: / and subroutine: blog_index")
	cookie = bottle.request.get_cookie("session")

	username = sessions.get_username(cookie)

	# todo: this is not yet implemented at this point in the course

	return bottle.template('blog_template', dict(username=username))



# displays the initial blog signup form
@bottle.get('/signup')
def present_signup():
	print("\n Under Route: /signup , method: get and subroutine: present signup")
	return bottle.template("signup",
						   dict(username="", password="",
								password_error="",
								email="", username_error="", email_error="",
								verify_error =""))

# displays the initial blog login form
@bottle.get('/login')
def present_login():
	print("\n Under Route: /login, method: get and subroutine: present_login")
	return bottle.template("login",
						   dict(username="", password="",
								login_error=""))

# handles a login request
@bottle.post('/login')
def process_login():
	print("\n Under Route: /login, method: post and subroutine: process_login")

	username = bottle.request.forms.get("username")
	password = bottle.request.forms.get("password")
	
	

	print ("\n user submitted ", username, "pass ", password)

	user_record = users.validate_login(username, password)
	if user_record:
		# username is stored in the user collection in the _id key
		session_id = sessions.start_session(user_record['_id'])

		if session_id is None:
			print("\n Under Route: /login, method: post and redirecting subroutine: /internal error ")
			bottle.redirect("/internal_error")

		cookie = session_id

		# Warning, if you are running into a problem whereby the cookie being set here is
		# not getting set on the redirect, you are probably using the experimental version of bottle (.12).
		# revert to .11 to solve the problem.
		bottle.response.set_cookie("session", cookie)
		
		print("\n Under Route: /login, method: post and redirecting subroutine: /welcome ")
		bottle.redirect("/welcome")

	else:
		print("\n Under Route: /login, method: post and User Record doesnt exist ")
		return bottle.template("login",
							   dict(username=cgi.escape(username), password="",
									login_error="Invalid Login"))


@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
	return {'error':"System has encountered a DB error"}


@bottle.get('/logout')
def process_logout():
	print("\n Under Route: /logout, method: get and subroutine: process_logout")

	cookie = bottle.request.get_cookie("session")

	print("\n calling the session object and destructing the cookies in Mongodb ")
	sessions.end_session(cookie)

	print("\n Setting up the cookies to blank")
	bottle.response.set_cookie("session", "")

	print("\n Under Route: /logout, method: get and redirecting subroutine: /signup ")
	bottle.redirect("/signup")


@bottle.post('/signup')
def process_signup():
	print("\n Under Route: /signup, method: post and subroutine: process_signup ")

	email = bottle.request.forms.get("email")
	username = bottle.request.forms.get("username")
	password = bottle.request.forms.get("password")
	verify = bottle.request.forms.get("verify")

	# set these up in case we have an error case
	errors = {'username': cgi.escape(username), 'email': cgi.escape(email)}
	if validate_signup(username, password, verify, email, errors):

		if not users.add_user(username, password, email):
			# this was a duplicate
			errors['username_error'] = "Username already in use. Please choose another"
			return bottle.template("signup", errors)

		session_id = sessions.start_session(username)
		print ("\n Printing the Session Id: ", session_id)
		bottle.response.set_cookie("session", session_id)
		print("\n Under Route: /signup, method: post and redirecting subroutine: /welcome ")
		bottle.redirect("/welcome")
	else:
		print ("user did not validate")
		return bottle.template("signup", errors)



@bottle.get("/welcome")
def present_welcome():
	# check for a cookie, if present, then extract value
	print("\n Under Route: /welcome, method: get and subroutine: present_welcome ")

	cookie = bottle.request.get_cookie("session")
	username = sessions.get_username(cookie)  # see if user is logged in
	if username is None:
		print ("\n welcome: can't identify user...redirecting to signup")
		bottle.redirect("/signup")

	return bottle.template("welcome", {'username': username})



# Helper Functions

# validates that the user information is valid for new signup, return True of False
# and fills in the error string if there is an issue
def validate_signup(username, password, verify, email, errors):
	print("\n Under Route: Helper, method invocation and subroutine: validate_signup ")
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	PASS_RE = re.compile(r"^.{3,20}$")
	EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

	errors['username_error'] = ""
	errors['password_error'] = ""
	errors['verify_error'] = ""
	errors['email_error'] = ""

	if not USER_RE.match(username):
		errors['username_error'] = "invalid username. try just letters and numbers"
		return False

	if not PASS_RE.match(password):
		errors['password_error'] = "invalid password."
		return False
	if password != verify:
		errors['verify_error'] = "password must match"
		return False
	if email != "":
		if not EMAIL_RE.match(email):
			errors['email_error'] = "invalid email address"
			return False
	return True

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.blog

users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)


bottle.debug(True)
bottle.run(host='localhost', port=8082)			# Start the webserver running and wait for requests

