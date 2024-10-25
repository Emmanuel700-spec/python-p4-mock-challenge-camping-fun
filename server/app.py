from flask import Flask, jsonify, request, abort
from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db.init_app(app)

@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([{"id": camper.id, "name": camper.name, "age": camper.age} for camper in campers])

@app.route('/campers/<int:id>', methods=['GET'])
def get_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404
    return jsonify({
        "id": camper.id,
        "name": camper.name,
        "age": camper.age,
        "signups": [signup.to_dict() for signup in camper.signups]
    })

@app.route('/campers', methods=['POST'])
def create_camper():
    data = request.json
    new_camper = Camper(name=data['name'], age=data['age'])
    errors = new_camper.validate()
    if errors:
        return jsonify({"errors": errors}), 400
    db.session.add(new_camper)
    db.session.commit()
    return jsonify({"id": new_camper.id, "name": new_camper.name, "age": new_camper.age}), 201

@app.route('/campers/<int:id>', methods=['PATCH'])
def update_camper(id):
    camper = Camper.query.get(id)
    if not camper:
        return jsonify({"error": "Camper not found"}), 404

    data = request.json
    camper.name = data.get('name', camper.name)
    camper.age = data.get('age', camper.age)
    errors = camper.validate()
    if errors:
        return jsonify({"errors": errors}), 400
    db.session.commit()
    return jsonify({"id": camper.id, "name": camper.name, "age": camper.age})

# Add additional routes for Activities and Signups...
