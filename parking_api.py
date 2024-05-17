from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['database_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

CORS(app)

class Space(db.Model):
    floor = db.Column(db.Integer, primary_key=True)
    spot = db.Column(db.String(1), primary_key=True)
    used = db.Column(db.Boolean, default=False)

@app.route('/api/parking/space', methods=['GET', 'POST'])
def parking_space():
    if request.method == 'GET':
        space = Space.query.all()
        result = [{'floor': space.floor, 'spot': space.spot.upper(), 'used': space.used}
                  for space in space]
        return jsonify(result)
    elif request.method == 'POST':
        data = request.get_json()
        space = Space(**data)
        db.session.add(space)
        db.session.commit()
        return jsonify({'message': 'Parking Space Created Successfully'}), 201

@app.route('/api/parking/space/<int:floor>/<string:spot>', methods=['GET', 'PUT', 'DELETE'])
def parking_space_specific(floor, spot):
    space = Space.query.get((floor, spot))
    if not space:
        return jsonify({'message': 'Space not found'}), 404

    if request.method == 'GET':
        result = {'floor': space.floor, 'spot': space.spot.upper(), 'used': space.used}
        return jsonify(result)

    elif request.method == 'PUT':
        data = request.get_json()
        space.used = data.get('used', space.used)
        db.session.commit()
        return jsonify({'message': 'Parking Space Updated Successfully'})

    elif request.method == 'DELETE':
        db.session.delete(space)
        db.session.commit()
        return jsonify({'message': 'Parking Space Deleted Successfully'})

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
