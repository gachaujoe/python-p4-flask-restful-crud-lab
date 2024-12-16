#!/usr/bin/env python3

# from flask import Flask, jsonify, request, make_response
# from flask_migrate import Migrate
# from flask_restful import Api, Resource

# from models import db, Plant

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)
# db.init_app(app)

# api = Api(app)


# class Plants(Resource):

#     def get(self):
#         plants = [plant.to_dict() for plant in Plant.query.all()]
#         return make_response(jsonify(plants), 200)

#     def post(self):
#         data = request.get_json()

#         new_plant = Plant(
#             name=data['name'],
#             image=data['image'],
#             price=data['price'],
#         )

#         db.session.add(new_plant)
#         db.session.commit()

#         return make_response(new_plant.to_dict(), 201)


# api.add_resource(Plants, '/plants')


# class PlantByID(Resource):

#     def get(self, id):
#         plant = Plant.query.filter_by(id=id).first().to_dict()
#         return make_response(jsonify(plant), 200)


# api.add_resource(PlantByID, '/plants/<int:id>')


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask app and SQLAlchemy instance
app = Flask(__name__)

# Configure the app for the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'  # Example using SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # To disable Flask-SQLAlchemy's modification tracking

# Initialize the SQLAlchemy object with the app
db = SQLAlchemy(app)

# Define the Plant model
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_in_stock = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": self.price,
            "is_in_stock": self.is_in_stock,
        }

# Route to update a plant
@app.route('/plants/<int:id>', methods=['PATCH'])
def update_plant(id):
    plant = Plant.query.get_or_404(id)
    data = request.get_json()

    # Update the plant if necessary
    if "is_in_stock" in data:
        plant.is_in_stock = data["is_in_stock"]
    
    db.session.commit()  # Save the changes to the database

    return jsonify(plant.to_dict()), 200

# Route to delete a plant
@app.route('/plants/<int:id>', methods=['DELETE'])
def delete_plant(id):
    plant = Plant.query.get_or_404(id)
    db.session.delete(plant)  # Remove the plant from the database
    db.session.commit()  # Commit the deletion

    return '', 204  # No content response

if __name__ == "__main__":
    app.run(debug=True)

