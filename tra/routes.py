from tra import db, app
from tra.models import UserData
from flask import redirect, request, session, render_template, flash, escape, url_for

@app.route("/")
@app.route("/home")
def home():
    if "name" not in session:
        return redirect(url_for("login"))
    # if the session name exists but has nothing in it, redirect to login page
    if len(session["name"].split("-")) != 2:
        return redirect(url_for("login"))
    return render_template("home.html")

@app.route("/login")
def login():
    if "firstname" in request.form and "lastname" in request.form: 
        # Add the user's name to the session 
        session["name"] = escape(f"{request.form['firstname']}-{request.form['lastname']}") 
        print(session)
        return redirect(url_for("home"))
        
    return render_template("login.html")

# This route is for testing writing to sql database
@app.route("/test", methods=["POST", "GET"])  # specify methods and route
def test():
	if request.method == "POST":
		session.permanent = True # set permanent session
		form_data = request.form["scout_data"]

		#found_user = users.query.filter_by(name=user).first() #what_to_access.perform_a_query.find_all_that_meet_criteria.grab_first_result    This is how to find a user
		usr_data = UserData(form_data)
		db.session.add(usr_data)
		db.session.commit()
		for i in UserData.query.all():
			print(i.data)

		flash("Data recieved!", "info")
	
	return render_template("scouting.html")
