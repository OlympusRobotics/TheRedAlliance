from tra import db, app
from tra.models import UserData
from flask import request, session, render_template, flash

@app.route("/", methods=["POST", "GET"])  # specify methods and route
def login():
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