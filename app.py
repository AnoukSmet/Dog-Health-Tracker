import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)


@app.route('/')
@app.route('/view_profile')
def view_profile():
    return render_template("dashboard.html", dogs=mongo.db.dogs.find())

@app.route('/add_dog')
def add_dog():
    return render_template("adddog.html")

@app.route('/insert_dog', methods=['POST'])
def insert_dog():
    dogs = mongo.db.dogs
    dogs.insert_one(request.form.to_dict())
    return redirect(url_for('view_profile'))

@app.route('/edit_profile/<dog_id>')
def edit_profile(dog_id):
    profile_to_update = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
    return render_template('editprofile.html', profile=profile_to_update)


@app.route('/update_profile/<dog_id>', methods=["POST"])
def update_profile(dog_id):
    dogs = mongo.db.dogs
    dogs.update({'_id': ObjectId(dog_id)}, 
    {
        'dog_name': request.form.get('dog_name'),
        'dog_breed': request.form.get('dog_breed'), 
        'date_of_birth': request.form.get('date_of_birth'), 
        'dog_description': request.form.get('dog_description')
    })
    return redirect(url_for('view_profile'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
