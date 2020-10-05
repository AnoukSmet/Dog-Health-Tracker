import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
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
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = generate_password_hash(request.form.get("password"))
 
        mongo.db.users.insert_one({
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password})

        if mongo.db.users.find_one({'username': username}) is not None:
            user = mongo.db.users.find_one({'username': username})
            user_id = user['_id']
            session['user_id'] = str(user_id)
            flash("Registration Successful!")
            return redirect(url_for("add_dog", user_id=user_id))

    return render_template("register.html")


@app.route('/sign_in', methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        # check if user already exists in db
        user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if user:
            if check_password_hash(user["password"],
               request.form.get("password")):
                user_id = user['_id']
                session['user_id'] = str(user_id)

                return redirect(url_for("view_dashboard",
                                        user_id=user_id))
            else:
                # invalid password match
                flash("Incorrect username and/or Password combination")
                return redirect(url_for("sign_in"))
        else:
            # Username doesn't exist
            flash("Incorrect username and/or Password combination")
            return redirect(url_for("sign_in"))

    return render_template("sign_in.html")


@app.route('/log_out')
def log_out():
    session.pop('user_id', None)
    return render_template('home.html')


@app.route('/view_dashboard/<user_id>')
def view_dashboard(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if user is None:
        return redirect(url_for('sign_in'))

    if session.get('user_id'):
        if session['user_id'] == str(user["_id"]):
            dogs = mongo.db.dogs.find({"user_id": user_id})
            # dog_id = str(dog["_id"])
            logs = mongo.db.logs.find()
            logs_count = logs.count()

        return render_template("dashboard.html",
                               user=user,
                               user_id=user_id,
                               dogs=dogs,
                               logs=logs,
                               logs_count=logs_count)


@app.route('/add_dog/<user_id>')
def add_dog(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("adddog.html", user_id=user_id, user=user)


@app.route('/insert_dog/<user_id>', methods=['POST'])
def insert_dog(user_id):
    dogs = mongo.db.dogs
    dogs.insert_one(request.form.to_dict())
    return redirect(url_for('view_dashboard', user_id=user_id))


@app.route('/edit_profile/<dog_id>')
def edit_profile(dog_id):
    profile_to_update = mongo.db.dogs.find_one({"_id": ObjectId(dog_id)})
    return render_template('editprofile.html', profile=profile_to_update)


@app.route('/update_profile/<dog_id>', methods=["POST"])
def update_profile(dog_id):
    dogs = mongo.db.dogs
    dogs.update({'_id': ObjectId(dog_id)}, {
        'dog_name': request.form.get('dog_name'),
        'dog_breed': request.form.get('dog_breed'),
        'date_of_birth': request.form.get('date_of_birth'),
        'dog_description': request.form.get('dog_description'),
        'image_url': request.form.get('image_url')
    })
    return redirect(url_for('view_dashboard'))


@app.route('/delete_profile/<dog_id>')
def delete_profile(dog_id):
    dogs = mongo.db.dogs
    dogs.remove({'_id': ObjectId(dog_id)})
    return redirect(url_for('view_dashboard'))


@app.route('/add_log/<user_id>/<dog_id>')
def add_log(user_id, dog_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    dog = mongo.db.dogs.find_one({"user_id": user_id})

    if session.get('user_id'):
        if session['user_id'] == str(user["_id"]):
            dog = mongo.db.dogs.find_one({"user_id": user_id})
            weight_metrics = mongo.db.weight_metrics.find()
            food_metrics = mongo.db.food_metrics.find()

    return render_template("addlog.html",
                           dog=dog,
                           weight_metrics=weight_metrics,
                           food_metrics=food_metrics,
                           user=user,
                           dog_id=dog_id,
                           user_id=user_id)


@app.route('/insert_log/<user_id>/<dog_id>', methods=['POST'])
def insert_log(user_id, dog_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user is None:
        return redirect(url_for('sign_in'))

    if session.get('user_id'):
        if session['user_id'] == str(user["_id"]):
            dog = mongo.db.dogs.find_one({"user_id": user_id})
            logs = mongo.db.logs
            logs.insert_one(request.form.to_dict())

    return redirect(url_for('view_dashboard',
                            user_id=user_id, dog=dog,
                            user=user))


@app.route('/edit_log/<log_id>')
def edit_log(log_id):
    log_to_update = mongo.db.logs.find_one({"_id": ObjectId(log_id)})
    return render_template('editlog.html',
                           log=log_to_update,
                           dogs=mongo.db.dogs.find(),
                           weight_metrics=mongo.db.weight_metrics.find(),
                           food_metrics=mongo.db.food_metrics.find())


@app.route('/update_log/<log_id>', methods=["POST"])
def update_log(log_id):
    logs = mongo.db.logs
    logs.update({'_id': ObjectId(log_id)}, {
        'dog_name': request.form.get('dog_name'),
        'log_date': request.form.get('log_date'),
        'dog_weight': request.form.get('dog_weight'),
        'weight_metric': request.form.get('weight_metric'),
        'dog_activity': request.form.get('dog_activity'),
        'dog_food': request.form.get('dog_food'),
        'food_metric': request.form.get('food_metric'),
        'other_notes': request.form.get('other_notes'),
    })
    return redirect(url_for('view_dashboard'))


@app.route('/delete_log/<log_id>')
def delete_log(log_id):
    logs = mongo.db.logs
    logs.remove({'_id': ObjectId(log_id)})
    return redirect(url_for('view_dashboard'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
