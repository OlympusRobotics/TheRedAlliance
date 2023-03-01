"These routes are JSON responses ONLY"
import re
import os
import json
import random
import string
from tra import db, limiter
from tra.helpers import authorized
from werkzeug.utils import secure_filename
from tra.models import Admin, Form, FormQuestion, Team, Response
from flask import Blueprint, request, render_template, session, jsonify, abort, flash

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/createform", methods=["GET"])
@limiter.limit("1/second;10/minute")
def create_form():
    """
    Create a new form and return its id.
    Limits each account to 15 forms
    JSON response
    """
    admin = authorized(session)
    if len(admin.forms) >= 100:
        abort(400, description="Form Limit Reached (100)")

    code = "".join(random.choice(string.ascii_letters) for _ in range(6))
    form = Form(
        admin=admin,
        code=code,
        json_repr=json.dumps(
            {"name": "FRC Scouting Form", "code": code,
                "draft": True, "questions": []}
        ),
    )

    db.session.add(form)
    db.session.commit()
    flash("Form Created!", "is-success")
    return {"msg": "Form Created", "code": form.code}


@bp.route("/editform/<code>", methods=["POST"])
@limiter.limit("3/second")
def edit_form(code):
    """
    Update a form. Takes JSON repr of the form
    Schema of JSON:
    {
        code : <len 6 str>,
        name : <str max len 15>,
        draft : <bool>,
        questions : [
            {
                code : <len 6 str>,
                type : <str questionType>,
                components : [
                    <basiclly anything can be put here>
                ]
            }
        ]
    }
    """
    admin = authorized(session)
    form = Form.query.filter_by(admin_id=admin.id, code=code).first_or_404()
    json_repr = request.json
    # validate and sanitize all the data
    if len(json_repr["name"]) > 40:
        abort(400, description="Form Title Too Long (40 max)")

    if type(json_repr["draft"]) != bool:
        abort(400)
    responses = []
    # TODO: make this not so stupid
    for q in form.questions:
        #     responses.append(q.responses)
        db.session.delete(q)
    db.session.commit()
    for q in json_repr["questions"]:
        form.questions.append(FormQuestion(
            code=q["code"], form=form, data=json.dumps(q)))
    db.session.commit()
    print(form.questions)

    # if empty name, make the name "Untitled Form"
    if len(json_repr["name"]) == 0:
        json_repr["name"] = "Untitled Form"
    form.json_repr = json.dumps(json_repr)
    form.draft = json_repr["draft"]
    form.name = json_repr["name"]
    db.session.commit()
    return {"status": 200}


@bp.route("/deleteform/<code>")
def delete_form(code):
    "Delete form with given code. Requires auth"
    admin = authorized(session)
    # filter for a form that has the same code and same admin id
    form = Form.query.filter_by(admin_id=admin.id, code=code).first_or_404()
    responses = Response.query.filter_by(form=form).all()
    teams = Team.query.filter_by(form=form).all()
    # remove all the questions
    for q in form.questions:
        db.session.delete(q)

    for r in responses:
        db.session.delete(r)

    for t in teams:
        db.session.delete(t)

    db.session.delete(form)
    db.session.commit()
    return {"status": 200}


@bp.route("/getform/<code>")
@limiter.limit("3/second")
def get_form_data(code):
    """Returns JSON repr of form"""
    # filter for a form that has the same code and same admin id
    form = Form.query.filter_by(code=code).first_or_404()
    return form.json_repr


@bp.route("/getforms", methods=["GET"])
@limiter.limit("2/second")
def get_forms():
    "Return list of form titles, codes, and draft state. Auth required"
    admin = authorized(session)
    forms = []
    for form in admin.forms:
        forms.append(
            {"code": form.code, "name": form.name, "draft": form.draft})

    return {"forms": forms}


@bp.route("/respond/<code>", methods=["POST"])
def respond(code):
    form = Form.query.filter_by(code=code).first_or_404()
    response = request.json["responses"]
    name = request.json["name"]
    team_num = request.json["teamNum"]
    team_data = Team.query.filter_by(number=team_num, form=form).first()
    # no responses found for this team number. Create a new Team row
    if team_data is None:
        team_data = Team(number=team_num, form=form)
        db.session.add(team_data)
        db.session.commit()

    db.session.add(Response(team=team_data, form_id=form.id,
                   name=name, data=json.dumps(response)))
    db.session.commit()

    return {'status': 200}


@bp.route("/getteamnums/<code>")
@limiter.limit("15/sec;80/minute")
def get_team_nums(code):
    """ Returns a list of team numbers for the given form """
    admin = authorized(session)
    form = Form.query.filter_by(code=code, admin=admin).first_or_404()
    return {"numbers":
            [team.number for team in form.teams]
            }


@bp.route("/getdata/<code>/<team_num>")
@limiter.limit("15/sec;80/minute")
def get_question_data(code, team_num):
    "Returns the response data for a question for a given form code"
    admin = authorized(session)
    form = Form.query.filter_by(code=code, admin=admin).first_or_404()
    team = Team.query.filter_by(number=team_num, form=form).first_or_404()

    return {"data":
            [
                {
                    "name": res.name,
                    "responses": json.loads(res.data),
                }
                for res in team.responses
            ]
            }


MIN_USER_LEN = 6


def validate_username(username):
    "query the username and check if it is valid. Returns a message which can be directly put into the HTML"

    msg = ""
    if len(username) > 60:
        msg = "Stop it u idiot"
    # username is taken
    elif not Admin.query.filter_by(username=username).first() is None:
        msg = "Email is taken"
    elif not re.match("[^@]+@[^@]+\.[^@]+", username):
        msg = "Email is not valid"
    return {"valid": msg}


@bp.route("/admin/is_username_valid", methods=["GET"])
@limiter.limit("4/sec")
def is_username_valid():
    """
    Wrapper for 'validate_username' function
    query the username and check if it is valid. Returns a message which can be directly put into the HTML
    """
    return validate_username(request.args["username"])


@bp.route("/uploadpfp/<form_code>/<team_num>", methods=['POST'])
def upload_photo(form_code, team_num):
    if 'pic' not in request.files:
        abort(400, description="No file")

    file = request.files['pic']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        abort(400, description="Empty Filename)")

    admin = authorized(session)
    form = Form.query.filter_by(admin=admin, code=form_code).first_or_404()
    team = Team.query.filter_by(form=form, number=team_num).first_or_404()

    if file:
        # save file
        filename = secure_filename(file.filename)
        file.save(os.path.join("tra/static/pictures/", filename))

        # update team pfp url
        team.pfp_url = "/static/pictures/" + filename
        db.session.commit()

        return jsonify(pfp=team.pfp_url), 200


@bp.route("/getprofiledata/<form_code>/<team_num>")
def get_profile_data(form_code, team_num):
    admin = authorized(session)
    team = Team.query.filter_by(number=team_num, form=Form.query.filter_by(
        admin=admin, code=form_code).first_or_404()).first_or_404()
    return jsonify(pfp=team.pfp_url, notes=team.notes), 200

@bp.route("/updatenotes/<form_code>/<team_num>", methods=["POST"])
def update_notes(form_code, team_num):
    admin = authorized(session)
    team = Team.query.filter_by(number=team_num, form=Form.query.filter_by(
        admin=admin, code=form_code).first_or_404()).first_or_404()

    team.notes = request.json['notes']
    db.session.commit()
    return jsonify(status=200), 200


@bp.errorhandler(429)
def rate_limited(e):
    return {"error": "Slow Down! Rate Limit Exceeded."}, 429


@bp.errorhandler(403)
def unauthorized(e):
    return {"error": "Unauthenticated. Please login again"}, 403


@bp.errorhandler(400)
def jsonify_error(e):
    return jsonify(error=e.description), 400
