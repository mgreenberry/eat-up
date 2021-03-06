import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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


@app.route("/")
@app.route("/catergories")
def catergories():
    catergories = mongo.db.catergories.find()
    return render_template("catergories.html", catergories=catergories)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return render_template("profile.html", username=username)


@app.route("/logout")
def logout():
    # Logs user out
    flash("You have logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_food", methods=["GET", "POST"])
def add_food():
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        food = {
            "food_name": request.form.get("food_name"),
            "food_group": request.form.get("food_group"),
            "use_by_date": request.form.get("use_by_date"),
            "barcode": request.form.get("barcode"),
            "is_urgent": is_urgent,
            "created_by": session["user"]
        }
        mongo.db.catergories.insert_one(food)
        flash("Food added succesfully")
        return redirect(url_for("add_food"))
        
    foods = mongo.db.catergories.find().sort("food_group", 1)
    return render_template("add_food.html", foods=foods)


@app.route("/edit_food/<food_name>", methods=["GET", "POST"])
def edit_food(food_name):

    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        submit = {
            "food_name": request.form.get("food_name"),
            "food_group": request.form.get("food_group"),
            "use_by_date": request.form.get("use_by_date"),
            "barcode": request.form.get("barcode"),
            "is_urgent": is_urgent,
            "created_by": session["user"]
        }
        mongo.db.catergories.update({"_id": ObjectId(food_name)}, submit)
        flash("Food updated succesfully")

    food = mongo.db.catergories.find_one({"_id": ObjectId(food_name)})
    foods = mongo.db.catergories.find().sort("food_name", 1)
    return render_template("edit_food.html", food=food, foods=foods)


@app.route("/delete_food/<food_name>")
def delete_food(food_name):
    mongo.db.catergories.remove({"_id": ObjectId(food_name)})
    flash("Food Deleted")
    return redirect(url_for("catergories"))


@app.route("/modifies")
def modifies():
    modifies = list(mongo.db.catergories.find().sort('use_by_date', 1))
    return render_template("modifies.html", modifies=modifies)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)