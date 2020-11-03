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
def home():
    """
    Function to load the homepage
    """
    return render_template('pages/home.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Allows the user to register at the website
    Checks if username already exists in Database
    Redirects user to the dashboard
    """
    if request.method == "POST":
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
            dogs = mongo.db.dogs.find({"user_id": user_id})
            count_dogs = dogs.count()
            return redirect(url_for("blank_dashboard", user_id=user_id,
                                    count_dogs=count_dogs))

    return render_template("pages/authentication.html", register=True)


@app.route('/signin', methods=["GET", "POST"])
def sign_in():
    """
    Allows user to sign in with username and password
    Redirects user to the dashboard
    """
    if request.method == "POST":
        user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user:
            if check_password_hash(user["password"],
               request.form.get("password")):
                user_id = str(user['_id'])
                session['user_id'] = str(user_id)

                dog_profile = mongo.db.dogs.find_one({"user_id": user_id})

                if dog_profile:
                    dog_id = dog_profile["_id"]
                    dogs = mongo.db.dogs.find({"user_id": user_id})
                    count_dogs = dogs.count()
                    return redirect(url_for("view_dashboard",
                                            user_id=user_id, dog_id=dog_id,
                                            count_dogs=count_dogs))

                else:
                    dogs = mongo.db.dogs.find({"user_id": user_id})
                    count_dogs = dogs.count()
                    return redirect(url_for("blank_dashboard",
                                            user_id=user_id,
                                            count_dogs=count_dogs))

            else:
                flash("Incorrect username and/or Password")
                return redirect(url_for("sign_in"))
        else:
            flash("Incorrect username and/or Password")
            return redirect(url_for("sign_in"))

    return render_template("pages/authentication.html")


@app.route('/logout')
def log_out():
    """
    Allows the user to log out
    Takes user back to home
    """
    session.pop('user_id', None)
    return render_template("pages/home.html")


@app.route('/dashboard/<user_id>')
def blank_dashboard(user_id):
    """
    When user has no dog profile added yet
    Blank dashboard will be displayed
    """
    dogs = mongo.db.dogs.find({"user_id": user_id})
    count_dogs = dogs.count()
    return render_template("pages/dashboard.html",
                           user_id=user_id,
                           count_dogs=count_dogs)


@app.route('/dashboard/<user_id>/<dog_id>', methods=["GET", "POST"])
def view_dashboard(user_id, dog_id):
    """
    When user has already at least 1 dog profile
    Dashboard of dog profile will be displayed
    """
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    dogs = mongo.db.dogs.find({"user_id": user_id})
    count_dogs = dogs.count()

    if user is None:
        return redirect(url_for('sign_in'))

    if session.get('user_id'):
        if session['user_id'] == str(user["_id"]):
            if request.method == 'POST':
                selected_profile = request.form.get('dog_name')
                dog_profile = mongo.db.dogs.find_one({
                                              "dog_name": selected_profile,
                                              "user_id": user_id})
                dog_id = str(dog_profile["_id"])
                logs = mongo.db.logs.find({'dog_id': dog_id}).sort(
                    'log_date', -1)
                count_logs = logs.count()

            else:
                dog_profile = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
                dog_id = str(dog_profile["_id"])
                logs = mongo.db.logs.find({'dog_id': dog_id}).sort(
                    'log_date', -1)
                count_logs = logs.count()

            return render_template("pages/dashboard.html",
                                   user_id=user_id,
                                   dogs=dogs,
                                   logs=logs,
                                   dog_id=dog_id,
                                   dog_profile=dog_profile,
                                   count_dogs=count_dogs,
                                   count_logs=count_logs)


@app.route('/logs/search/<user_id>/<dog_id>', methods=['GET', 'POST'])
def search_logs(user_id, dog_id):
    """
    Allows user to search logs by log date for specific dog
    """
    if request.method == "POST":
        log_date = request.form.get("log_date")
        logs = mongo.db.logs.find({"dog_id": dog_id,
                                   "log_date": log_date})
        count_logs = logs.count()

    logs = ''
    count_logs = logs.count(logs)

    return render_template("pages/searchlogs.html",
                           user_id=user_id,
                           dog_id=dog_id,
                           logs=logs,
                           count_logs=count_logs)


@app.route('/dog/add/<user_id>', methods=['GET', 'POST'])
def add_dog(user_id):
    """
    Allows the user to add a dog profile
    Redirects the user to the dashboard of that dog profile
    """
    if request.method == 'POST':
        dogs = mongo.db.dogs.find({"user_id": user_id})
        dog_profile = {
            'user_id': request.form.get('user_id'),
            'dog_name': request.form.get('dog_name'),
            'dog_breed': request.form.get('dog_breed'),
            'date_of_birth': request.form.get('date_of_birth'),
            'dog_description': request.form.get('dog_description'),
            'dog_image': request.form.get('dog_image')
        }
        mongo.db.dogs.insert_one(dog_profile)
        dog_profile = mongo.db.dogs.find_one({
             "dog_name": request.form.get('dog_name'),
             "user_id": request.form.get('user_id')})
        dog_id = dog_profile["_id"]
        count_dogs = dogs.count()
        return redirect(url_for("view_dashboard",
                                user_id=user_id, dog_id=dog_id,
                                count_dogs=count_dogs))

    dogs = mongo.db.dogs.find({"user_id": user_id})
    count_dogs = dogs.count()
    return render_template("pages/dogprofile.html", user_id=user_id,
                           count_dogs=count_dogs,
                           add=True)


@app.route('/dog/edit/<user_id>/<dog_id>', methods=['GET', 'POST'])
def edit_dog(user_id, dog_id):
    """
    Allows the user to edit / update a dog profile
    Redirects the user to the dashboard of the updated dog profile
    """
    if request.method == "POST":
        mongo.db.dogs.update({'_id': ObjectId(dog_id)}, {
            'user_id': request.form.get('user_id'),
            'dog_name': request.form.get('dog_name'),
            'dog_breed': request.form.get('dog_breed'),
            'date_of_birth': request.form.get('date_of_birth'),
            'dog_description': request.form.get('dog_description'),
            'dog_image': request.form.get('dog_image')
        })
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()
        return redirect(url_for('view_dashboard',
                                user_id=user_id,
                                dog_id=dog_id,
                                count_dogs=count_dogs))

    dog_profile = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
    dog_id = dog_profile["_id"]
    return render_template('pages/dogprofile.html',
                           dog_id=dog_id,
                           dog_profile=dog_profile,
                           user_id=user_id)


@app.route('/dog/delete/<user_id>/<dog_id>')
def delete_dog(user_id, dog_id):
    """
    Allows the user to delete a dog profile
    Redirects the user to the dashboard
    """
    dogs = mongo.db.dogs.find({"user_id": user_id})

    if dogs.count() > 1:
        mongo.db.dogs.remove({'_id': ObjectId(dog_id)})
        dog_profile = mongo.db.dogs.find_one({"user_id": user_id})
        dog_id = dog_profile["_id"]
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()
        return redirect(url_for('view_dashboard', user_id=user_id,
                                dog_id=dog_id,
                                count_dogs=count_dogs))

    else:
        mongo.db.dogs.remove({'_id': ObjectId(dog_id)})
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()
        return redirect(url_for("blank_dashboard", user_id=user_id,
                                count_dogs=count_dogs))


@app.route('/log/add/<user_id>/<dog_id>', methods=['GET', 'POST'])
def add_log(user_id, dog_id):
    """
    Allows the user the add logs for the relevant dog profile
    Redirects the user to the dashboard of the relevant dog
    """
    if request.method == "POST":
        mongo.db.logs.insert_one(request.form.to_dict())
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()

        return redirect(url_for('view_dashboard',
                                user_id=user_id, dog_id=dog_id,
                                count_dogs=count_dogs))

    weight_metrics = mongo.db.weight_metrics.find()
    food_metrics = mongo.db.food_metrics.find()

    return render_template("pages/logs.html",
                           weight_metrics=weight_metrics,
                           food_metrics=food_metrics,
                           dog_id=dog_id,
                           user_id=user_id,
                           add=True)


@app.route('/log/edit/<user_id>/<dog_id>/<log_id>',
           methods=['GET', 'POST'])
def edit_log(user_id, dog_id, log_id):
    """
    Allows the user to edit logs
    Redirects user to the dashboard
    """
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
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()
        return redirect(url_for('view_dashboard',
                                user_id=user_id,
                                dog_id=dog_id,
                                count_dogs=count_dogs))

    log_to_update = mongo.db.logs.find_one({"_id": ObjectId(log_id)})

    return render_template('pages/logs.html',
                           log=log_to_update,
                           dogs=mongo.db.dogs.find({"user_id": user_id}),
                           weight_metrics=mongo.db.weight_metrics.find(),
                           food_metrics=mongo.db.food_metrics.find(),
                           user_id=user_id,
                           dog_id=dog_id)


@app.route('/log/delete/<user_id>/<dog_id>/<log_id>')
def delete_log(user_id, dog_id, log_id):
    """
    Allows user the delete logs
    Redirect the user to the dashboard
    """
    mongo.db.logs.remove({'_id': ObjectId(log_id)})
    dogs = mongo.db.dogs.find({"user_id": user_id})
    count_dogs = dogs.count()
    return redirect(url_for('view_dashboard', user_id=user_id, dog_id=dog_id,
                            count_dogs=count_dogs))


@app.errorhandler(404)
def page_not_found(error):
    """
    Renders error.html with 404 message
    """
    error_message = str(error)
    return render_template('pages/error.html',
                           error_message=error_message), 404


@app.errorhandler(500)
def server_error(error):
    """
    Renders error.html with 500 message.
    """
    error_message = str(error)
    return render_template('pages/error.html',
                           error_message=error_message), 500


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=os.environ.get("DEBUG"))
