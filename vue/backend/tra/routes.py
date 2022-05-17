from tra.models import Scout
from tra import app, db


@app.route('/scouts')
def scouts():
    return {'scouts': [{'id': scout.id, 'name': scout.name, 'code': scout.code} for scout in Scout.query.all()]}
