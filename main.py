from __future__ import print_function

import sys

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)  # Initialze flask constructor

# Add your own details
config = {
    "apiKey": "AIzaSyBFneL-i7Vw7SN1Z5xb7awvyAPW_0NAABI",
    "authDomain": "hacathon-405514.firebaseapp.com",
    "projectId": "hacathon-405514",
    "storageBucket": "hacathon-405514.appspot.com",
    "messagingSenderId": "261356358269",
    "appId": "1:261356358269:web:314828cf1c22a08b547f14",
    "measurementId": "G-Y0DNHY70N6"
}

# initialize firebase
cred = credentials.Certificate("firestore/hacathon-405514-firebase-adminsdk-8k34v-49ee4584ff.json")
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()
# Initialze person as dictionary
person = {"is_logged_in": False, "email": ""}


# Login
@app.route("/")
def login():
    return render_template("login.html")


# Welcome page
@app.route("/welcome")
def welcome():
    if person["is_logged_in"]:
        return render_template("welcome.html", email=person["email"])
    else:
        return redirect(url_for('login'))


# If someone clicks on login, they are redirected to /result
@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":  # Only if data has been posted
        form = request.form  # Get the data
        email = form["email"]
        password = form["password"]
        try:
            doc_ref = db.collection('administrators').document(email)
            doc = doc_ref.get()
            if doc.exists:
                administrator = doc.to_dict().get("password")

                if administrator == password:  # success login scenario
                    global person
                    person["is_logged_in"] = True
                    person["email"] = email
                    return redirect(url_for('welcome'))

                return redirect(url_for('login'))  # log in failed
            else:
                # If there is any error, redirect back to login

                return redirect(url_for('login'))

        except:
            # If there is any error, redirect back to login
            # print("Autentificare nereușită!", file=sys.stderr)
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"]:
            return redirect(url_for('welcome'))
        else:
            print("Autentificare nereușită4!", file=sys.stderr)
            return redirect(url_for('login'))


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()