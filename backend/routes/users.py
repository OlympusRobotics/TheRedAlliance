from .. import db
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/create', methods=['POST'])
def create():
    pass

@bp.route('/delete', methods=["delete"])
def delete():
    pass

@bp.route('/getinfo')
def getinfo():
    pass
