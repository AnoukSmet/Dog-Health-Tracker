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
    return render_template('pages/home.html')


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

        # add user to the users collection in database
        mongo.db.users.insert_one({
            'username': username,
            'password': password})

        # when registration successfull, redirect to add dog form
        if mongo.db.users.find_one({'username': username}) is not None:
            user = mongo.db.users.find_one({'username': username})
            user_id = user['_id']
            session['user_id'] = str(user_id)
            dogs = mongo.db.dogs.find({"user_id": user_id})
            count_dogs = dogs.count()
            return redirect(url_for("blank_dashboard", user_id=user_id,
                                    count_dogs=count_dogs))

    return render_template("pages/register.html")


@app.route('/signin', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # check if user already exists in db
        user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        # if user exists, verify password
        if user:
            if check_password_hash(user["password"],
               request.form.get("password")):
                user_id = str(user['_id'])
                session['user_id'] = str(user_id)

                # find dog in dogs collection related to the user
                dog = mongo.db.dogs.find_one({"user_id": user_id})

                # check if user already has a dog_profile added to its account
                if dog:
                    # If yes, show dashboard of dog profile
                    dog_id = dog["_id"]
                    dogs = mongo.db.dogs.find({"user_id": user_id})
                    count_dogs = dogs.count()
                    return redirect(url_for("view_dashboard",
                                            user_id=user_id, dog_id=dog_id,
                                            count_dogs=count_dogs))

                else:
                    # If no, redirect user to blank_dashboard
                    dogs = mongo.db.dogs.find({"user_id": user_id})
                    count_dogs = dogs.count()
                    return redirect(url_for("blank_dashboard",
                                            user_id=user_id,
                                            count_dogs=count_dogs))

            else:
                # invalid password match
                flash("Incorrect username and/or Password")
                return redirect(url_for("sign_in"))
        else:
            # Username doesn't exist
            flash("Incorrect username and/or Password")
            return redirect(url_for("sign_in"))

    return render_template("pages/sign_in.html")


@app.route('/logout')
def log_out():
    session.pop('user_id', None)
    return render_template("pages/home.html")


@app.route('/dashboard/<user_id>')
def blank_dashboard(user_id):
    dogs = mongo.db.dogs.find({"user_id": user_id})
    count_dogs = dogs.count()
    return render_template("pages/dashboard.html",
                           user_id=user_id,
                           count_dogs=count_dogs)


@app.route('/dashboard/<user_id>/<dog_id>', methods=["GET", "POST"])
def view_dashboard(user_id, dog_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    dogs = mongo.db.dogs.find({"user_id": user_id})
    # Get count of dogs do display select box when more than 1 dog
    # When only 1 dog, disable delete dog button
    count_dogs = dogs.count()

    if user is None:
        return redirect(url_for('sign_in'))

    if session.get('user_id'):
        if session['user_id'] == str(user["_id"]):
            if request.method == 'POST':
                # Receive input from user which profile should be displayed
                selected_profile = request.form.get('dog_name')
                dog = mongo.db.dogs.find_one({"dog_name": selected_profile,
                                              "user_id": user_id})
                dog_id = str(dog["_id"])
                logs = mongo.db.logs.find({'dog_id': dog_id}).sort(
                    "log_date", -1)
                count_logs = logs.count()

            else:
                # if no input was given, find dog related to user
                dog = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
                dog_id = str(dog["_id"])
                logs = mongo.db.logs.find({'dog_id': dog_id}).sort(
                    "log_date", -1)
                count_logs = logs.count()

            return render_template("pages/dashboard.html",
                                   user_id=user_id,
                                   dogs=dogs,
                                   logs=logs,
                                   dog_id=dog_id,
                                   dog=dog,
                                   count_dogs=count_dogs,
                                   count_logs=count_logs)


@app.route('/api/logs/search/<user_id>/<dog_id>', methods=['GET', 'POST'])
def search_logs(user_id, dog_id):
    if request.method == "POST":
        # Get date input from user
        log_date = request.form.get("log_date")

        # find logs where input matches the log_date from relevant dog
        logs = mongo.db.logs.find({"dog_id": dog_id,
                                   "log_date": log_date})
        count_logs = logs.count()

    elif request.method == 'GET':
        # when no input is given yet, no logs should be displayed
        logs = ''
        count_logs = logs.count(logs)

    return render_template("pages/searchlogs.html",
                           user_id=user_id,
                           dog_id=dog_id,
                           logs=logs,
                           count_logs=count_logs)


@app.route('/api/dog/add/<user_id>', methods=['GET', 'POST'])
def add_dog(user_id):

    if request.method == 'POST':
        # when form was submitted, retrieve input
        dogs = mongo.db.dogs.find({"user_id": user_id})
        dog = {
            'user_id': request.form.get('user_id'),
            'dog_name': request.form.get('dog_name'),
            'dog_breed': request.form.get('dog_breed'),
            'date_of_birth': request.form.get('date_of_birth'),
            'dog_description': request.form.get('dog_description'),
            'dog_image': request.form.get('dog_image')
        }
        # store input in dogs collection in database
        mongo.db.dogs.insert_one(dog)
        # find inserted dog and redirect to dashboard of inserted dog
        dog = mongo.db.dogs.find_one({
             "dog_name": request.form.get('dog_name'),
             "user_id": request.form.get('user_id')})
        dog_id = dog["_id"]
        count_dogs = dogs.count()
        return redirect(url_for("view_dashboard",
                                user_id=user_id, dog_id=dog_id,
                                count_dogs=count_dogs))

    elif request.method == 'GET':
        # Get count of dogs related to user
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()
        # if count is not equal to 0,
        # get dog_id for in case user clicks cancel button
        if count_dogs != 0:
            dog = mongo.db.dogs.find_one({"user_id": user_id})
            dog_id = dog["_id"]
            return render_template("pages/adddog.html", user_id=user_id,
                                   dog_id=dog_id,
                                   count_dogs=count_dogs)
        # if count is 0,
        # no need to get dog_id as blank_dashboard doesn't require dog_id
        else:
            return render_template("pages/adddog.html", user_id=user_id,
                                   count_dogs=count_dogs)


@app.route('/api/dog/edit/<user_id>/<dog_id>', methods=['GET', 'POST'])
def edit_dog(user_id, dog_id):
    if request.method == "POST":
        # Update dog profile with input received from user
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

    elif request.method == "GET":
        # Get dog profile that needs to be updated
        dog = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
        dog_id = dog["_id"]
        return render_template('pages/editdog.html',
                               dog_id=dog_id,
                               dog=dog,
                               user_id=user_id)


@app.route('/api/dog/delete/<user_id>/<dog_id>')
def delete_dog(user_id, dog_id):
    # Find all the dogs that fall under the user account
    dogs = mongo.db.dogs.find({"user_id": user_id})

    # If the user has more than 1 dog profile, remove dog profile
    # Find remaining dog related to user to display on dashboard
    if dogs.count() > 1:
        mongo.db.dogs.remove({'_id': ObjectId(dog_id)})
        dog = mongo.db.dogs.find_one({"user_id": user_id})
        dog_id = dog["_id"]
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()
        return redirect(url_for('view_dashboard', user_id=user_id,
                                dog_id=dog_id,
                                count_dogs=count_dogs))

    # If user only has 1 dog remaining, redirect user to add_dog
    else:
        mongo.db.dogs.remove({'_id': ObjectId(dog_id)})
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()
        return redirect(url_for("blank_dashboard", user_id=user_id,
                                count_dogs=count_dogs))


@app.route('/api/log/add/<user_id>/<dog_id>', methods=['GET', 'POST'])
def add_log(user_id, dog_id):
    if request.method == "POST":
        # Add log to logs collection in database
        mongo.db.logs.insert_one(request.form.to_dict())
        dogs = mongo.db.dogs.find({"user_id": user_id})
        count_dogs = dogs.count()

        return redirect(url_for('view_dashboard',
                                user_id=user_id, dog_id=dog_id,
                                count_dogs=count_dogs))

    elif request.method == "GET":
        # Get metric for weight and food input
        weight_metrics = mongo.db.weight_metrics.find()
        food_metrics = mongo.db.food_metrics.find()

        return render_template("pages/addlog.html",
                               weight_metrics=weight_metrics,
                               food_metrics=food_metrics,
                               dog_id=dog_id,
                               user_id=user_id)


@app.route('/api/log/edit/<user_id>/<dog_id>/<log_id>',
           methods=['GET', 'POST'])
def edit_log(user_id, dog_id, log_id):
    # Update log with input received from user
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

    elif request.method == 'GET':
        # find log that needs to be updated
        log_to_update = mongo.db.logs.find_one({"_id": ObjectId(log_id)})

        return render_template('pages/editlog.html',
                               log=log_to_update,
                               dogs=mongo.db.dogs.find({"user_id": user_id}),
                               weight_metrics=mongo.db.weight_metrics.find(),
                               food_metrics=mongo.db.food_metrics.find(),
                               user_id=user_id,
                               dog_id=dog_id)


@app.route('/api/log/delete/<user_id>/<dog_id>/<log_id>')
def delete_log(user_id, dog_id, log_id):
    # Find log that needs to be deleted
    mongo.db.logs.remove({'_id': ObjectId(log_id)})
    dogs = mongo.db.dogs.find({"user_id": user_id})
    count_dogs = dogs.count()
    return redirect(url_for('view_dashboard', user_id=user_id, dog_id=dog_id,
                            count_dogs=count_dogs))


@app.errorhandler(404)
def page_not_found(error):
    # Renders error.html with 404 message.
    error_message = str(error)
    return render_template('pages/error.html',
                           error_message=error_message), 404


@app.errorhandler(500)
def server_error(error):
    # Renders error.html with 500 message.
    error_message = str(error)
    return render_template('pages/error.html',
                           error_message=error_message), 500


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
