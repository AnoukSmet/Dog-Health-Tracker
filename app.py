import os
from flask import (Flask, render_template, redirect, request, url_for, session,
                   flash)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # check if user already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        username = request.form.get("username").lower()
        password = generate_password_hash(request.form.get("password"))

        mongo.db.users.insert_one({
            'username': username,
            'password': password})

        if mongo.db.users.find_one({'username': username}) is not None:
            user = mongo.db.users.find_one({'username': username})
            user_id = user['_id']
            session['user_id'] = str(user_id)
            flash("Registration Successful!")
            return redirect(url_for("add_dog", user_id=user_id))

    return render_template("register.html")


@app.route('/signin', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # check if user already exists in db
        user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user:
            if check_password_hash(user["password"],
               request.form.get("password")):
                user_id = str(user['_id'])
                session['user_id'] = str(user_id)
                dog = mongo.db.dogs.find_one({"user_id": user_id})
                dog_id = dog["_id"]

                return redirect(url_for("view_dashboard",
                                        user_id=user_id, dog_id=dog_id))
            else:
                # invalid password match
                flash("Incorrect username and/or Password combination")
                return redirect(url_for("sign_in"))
        else:
            # Username doesn't exist
            flash("Incorrect username and/or Password combination")
            return redirect(url_for("sign_in"))

    return render_template("sign_in.html")


@app.route('/logout')
def log_out():
    session.pop('user_id', None)

    return render_template('home.html')


@app.route('/dashboard/<user_id>/<dog_id>', methods=["GET", "POST"])
def view_dashboard(user_id, dog_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    dogs = mongo.db.dogs.find({"user_id": user_id})
    count_dogs = dogs.count()

    if user is None:
        return redirect(url_for('sign_in'))

    if session.get('user_id'):
        if session['user_id'] == str(user["_id"]):
            if request.method == 'POST':
                selected_profile = request.form.get('dog_name')
                dog = mongo.db.dogs.find_one({"dog_name": selected_profile})
                dog_id = str(dog["_id"])
                logs = mongo.db.logs.find({"dog_id": dog_id})
                count_logs = logs.count()
            else:
                dog = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
                dog_id = str(dog["_id"])
                logs = mongo.db.logs.find({"dog_id": dog_id})
                count_logs = logs.count()

            return render_template("dashboard.html",
                                   user_id=user_id,
                                   dogs=dogs,
                                   logs=logs,
                                   dog_id=dog_id,
                                   dog=dog,
                                   count_dogs=count_dogs,
                                   count_logs=count_logs)


@app.route('/api/dog/add/<user_id>', methods=['GET', 'POST'])
def add_dog(user_id):

    if request.method == 'POST':
        dog = {
            'user_id': request.form.get('user_id'),
            'dog_name': request.form.get('dog_name'),
            'dog_breed': request.form.get('dog_breed'),
            'date_of_birth': request.form.get('date_of_birth'),
            'dog_description': request.form.get('dog_description'),
            'dog_image': request.form.get('dog_image')
        }
        mongo.db.dogs.insert_one(dog)
        dog = mongo.db.dogs.find_one({
             "dog_name": request.form.get('dog_name')})
        dog_id = dog["_id"]
        return redirect(url_for("view_dashboard",
                                user_id=user_id, dog_id=dog_id))

    elif request.method == 'GET':
        dogs = mongo.db.dogs.find({"user_id": user_id})
        total_dogs = dogs.count()
        return render_template("adddog.html", user_id=user_id,
                               dogs=total_dogs)


@app.route('/api/dog/edit/<user_id>/<dog_id>', methods=['GET', 'POST'])
def edit_dog(user_id, dog_id):
    if request.method == "POST":
        mongo.db.dogs.update({'_id': ObjectId(dog_id)}, {
            'user_id': request.form.get('user_id'),
            'dog_name': request.form.get('dog_name'),
            'dog_breed': request.form.get('dog_breed'),
            'date_of_birth': request.form.get('date_of_birth'),
            'dog_description': request.form.get('dog_description'),
            'dog_image': request.form.get('dog_image')
        })
        return redirect(url_for('view_dashboard',
                                user_id=user_id,
                                dog_id=dog_id))

    elif request.method == "GET":
        profile_to_update = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
        return render_template('editdog.html',
                               profile=profile_to_update,
                               user_id=user_id)


@app.route('/api/dog/delete/<user_id>/<dog_id>')
def delete_dog(user_id, dog_id):
    mongo.db.dogs.remove({'_id': ObjectId(dog_id)})
    mongo.db.logs.remove({'dog_id': ObjectId(dog_id)})
    dog = mongo.db.dogs.find_one({"user_id": user_id})
    dog_id = dog["_id"]
    return redirect(url_for('view_dashboard', user_id=user_id, dog_id=dog_id))


@app.route('/api/log/add/<user_id>/<dog_id>', methods=['GET', 'POST'])
def add_log(user_id, dog_id):

    if request.method == "POST":
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        dog = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
        if user is None:
            return redirect(url_for('sign_in'))

        if session.get('user_id'):
            if session['user_id'] == str(user["_id"]):
                dog = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
                logs = mongo.db.logs
                logs.insert_one(request.form.to_dict())

        return redirect(url_for('view_dashboard',
                                user_id=user_id, dog=dog, dog_id=dog_id))

    elif request.method == "GET":

        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

        if session.get('user_id'):
            if session['user_id'] == str(user["_id"]):
                weight_metrics = mongo.db.weight_metrics.find()
                food_metrics = mongo.db.food_metrics.find()

        return render_template("addlog.html",
                               weight_metrics=weight_metrics,
                               food_metrics=food_metrics,
                               dog_id=dog_id,
                               user_id=user_id)


@app.route('/api/log/edit/<user_id>/<dog_id>/<log_id>',
           methods=['GET', 'POST'])
def edit_log(user_id, dog_id, log_id):
    if request.method == "POST":
        mongo.db.logs.update({'_id': ObjectId(log_id)}, {
            'user_id': request.form.get('user_id'),
            'dog_id': request.form.get('dog_id'),
            'dog_name': request.form.get('dog_name'),
            'log_date': request.form.get('log_date'),
            'dog_weight': request.form.get('dog_weight'),
            'weight_metric': request.form.get('weight_metric'),
            'dog_activity': request.form.get('dog_activity'),
            'dog_food': request.form.get('dog_food'),
            'food_metric': request.form.get('food_metric'),
            'other_notes': request.form.get('other_notes'),
        })
        return redirect(url_for('view_dashboard',
                                user_id=user_id,
                                dog_id=dog_id))

    elif request.method == 'GET':
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        user_id = user["_id"]
        log_to_update = mongo.db.logs.find_one({"_id": ObjectId(log_id)})
        return render_template('editlog.html',
                               log=log_to_update,
                               dogs=mongo.db.dogs.find({"user_id": user_id}),
                               weight_metrics=mongo.db.weight_metrics.find(),
                               food_metrics=mongo.db.food_metrics.find(),
                               user_id=user_id,
                               dog_id=dog_id)


@app.route('/api/log/delete/<user_id>/<dog_id>/<log_id>')
def delete_log(user_id, dog_id, log_id):
    mongo.db.logs.remove({'_id': ObjectId(log_id)})
    return redirect(url_for('view_dashboard', user_id=user_id, dog_id=dog_id))


@app.route('/api/profile/delete/<user_id>')
def delete_profile(user_id):
    mongo.db.logs.remove({"user_id": ObjectId(user_id)})
    mongo.db.dogs.remove({"user_id": ObjectId(user_id)})
    mongo.db.users.remove({'_id': ObjectId(user_id)})
    return render_template('home.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
