from __future__ import print_function

import sys

import firebase_admin
from PIL import Image
from firebase_admin import credentials, firestore
from flask import Flask, redirect, render_template, request, url_for

from ai_lib import id_img_to_text, image_path_to_np_array, request_json_from_id_text

app = Flask(__name__)  # Initialze flask constructor

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
    """
    image_path = 'static/coco.jpeg'
    print(request_json_from_id_text(id_img_to_text(image_path_to_np_array(image_path))))
    """

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
