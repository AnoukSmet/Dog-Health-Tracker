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
    return render_template("dashboard.html", dogs=mongo.db.dogs.find(), logs=mongo.db.logs.find())

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


@app.route('/add_log')
def add_log():
    return render_template("addlog.html")


@app.route('/insert_log', methods=['POST'])
def insert_log():
    logs = mongo.db.logs
    logs.insert_one(request.form.to_dict())
    return redirect(url_for('view_profile'))


@app.route('/edit_log/<log_id>')
def edit_log(log_id):
    log_to_update = mongo.db.logs.find_one({"_id": ObjectId(log_id)})
    return render_template('editlog.html', log=log_to_update)



@app.route('/update_log/<log_id>', methods=["POST"])
def update_log(log_id):
    logs = mongo.db.logs
    logs.update({'_id': ObjectId(log_id)}, 
    {
        'log_date': request.form.get('log_date'),
        'dog_weigth': request.form.get('dog_weigth'), 
        'dog_activity': request.form.get('dog_activity'), 
        'dog_food': request.form.get('dog_food'),
        'other_notes': request.form.get('other_notes')
    })
    return redirect(url_for('view_profile'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
