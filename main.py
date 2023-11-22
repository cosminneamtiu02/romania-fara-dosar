from __future__ import print_function

import json
import os
import sys

import cv2
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, redirect, render_template, request, url_for

from ai_lib import photo_to_json, crop_face_from_id, data_url_to_cv2
from firestore_utils import commit_image_to_firestore, commit_person_to_firestore

app = Flask(__name__)  # Initialze flask constructor

# initialize firebase
cred = credentials.Certificate("firestore/hacathon-405514-firebase-adminsdk-8k34v-49ee4584ff.json")
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()
# Initialze person as dictionary
person = {"is_logged_in": False, "email": ""}
id_data = {}


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
            return redirect(url_for('login'))


@app.route("/data_display", methods=["POST", "GET"])
def data_display():
    if request.method == "POST":
        try:

            image_data = request.form.get("image_data")

            id_json_data = json.loads(photo_to_json(image_data))
            id_json_data['email'] = ''
            id_json_data['phone_number'] = ''
            id_json_data['password'] = ''

            id_image = crop_face_from_id(image_data)
            cv2.imwrite("static/" + id_json_data["cnp"] + "_face.png", id_image)
            cv2.imwrite("static/" + id_json_data["cnp"] + "_id.png", data_url_to_cv2(image_data))

            id_json_data['face_photo'] = "static/" + id_json_data["cnp"] + "_face.png"
            id_json_data['id_photo'] = "static/" + id_json_data["cnp"] + "_id.png"

            return render_template("id_data_display.html",
                                   cnp=id_json_data["cnp"],
                                   series=id_json_data["series"],
                                   number=id_json_data["number"],
                                   name=id_json_data["name"],
                                   surname=id_json_data["surname"],
                                   citizenship=id_json_data["citizenship"],
                                   place_of_birth=id_json_data["place_of_birth"],
                                   address=id_json_data["adress"],
                                   authority=id_json_data["authority"],
                                   date_issued=id_json_data["date issued"],
                                   valid_until=id_json_data["valid_until"],
                                   sex=id_json_data["sex"],
                                   id_image=id_json_data['face_photo'],
                                   id_photo=id_json_data['id_photo']
                                   )

        except:
            return redirect(url_for('welcome'))

@app.route('/commit_data', methods=['POST', 'GET'])
def commit_data():
    if request.method == "POST":
        person_dictionary = {'cnp': request.form.get('cnp'),
                             'series': request.form.get('series'),
                             'number': request.form.get('number'),
                             'name': request.form.get('name'),
                             'surname': request.form.get('surname'),
                             'citizenship': request.form.get('citizenship'),
                             'birth_place': request.form.get('birth_place'),
                             'address': request.form.get('address'),
                             'authority': request.form.get('authority'),
                             'availability': request.form.get('availability'),
                             'valid_until': request.form.get('valid_until'),
                             'sex': request.form.get('sex'),
                             'email': request.form.get('email'),
                             'phone_nr': request.form.get('phone_nr')}

        #print(person_dictionary, file=sys.stderr)

        face_photo = "static/" + person_dictionary["cnp"] + "_face.png"
        id_photo = "static/" + person_dictionary["cnp"] + "_id.png"
    
        commit_person_to_firestore(person_dictionary,
                                   face_photo,
                                   id_photo)
    
        os.remove(face_photo)
        os.remove(id_photo)

        return redirect(url_for('welcome'))

if __name__ == "__main__":

    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
