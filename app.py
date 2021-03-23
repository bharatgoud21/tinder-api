import firebase_admin
from firebase_admin import auth, firestore, storage, credentials
import flask
from flask import abort, jsonify, request, redirect
import json
import requests

app = flask.Flask(__name__)

cred = credentials.Certificate("tinder-e36bd-firebase-adminsdk-q00sb-adb4618c67.json")
firebase_app = firebase_admin.initialize_app(cred)
store = firestore.client()


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    emailOfUser = data.get("email")
    uid = " "
    message = " "
    try:
        user = auth.get_user_by_email(emailOfUser)
        message = "SuccessFully Got The User"
        uid = user.uid
    except:
        message = "User Not There in FIREBASE!!"

    return jsonify({"Response": 200, "uid": uid, "message": message})


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json(force=True)

    emailOfUser = data.get("email")
    passwordOfUser = data.get("password")
    uid = " "
    message = " "
    try:
        user = auth.create_user(
            email=emailOfUser,
            email_verified=False,
            password=passwordOfUser
        )
        message = "SuccessFully Created A NEW USER!!!"
        uid = user.uid
    except:
        message = "User Already There in FIREBASE!!"

    return jsonify({"Response": 200, "uid": uid, "message": message})


@app.route('/updateUser', methods=['POST'])
def updateUser(uid,dit):
    dit = request.get_json(force=True)

    uid = dit['uid']
    dit_user_details = {}
    dit_user_details['name'] = dit["name"]
    dit_user_details['email'] = dit["email"]
    dit_user_details['number'] = dit["number"]
    dit_user_details['image'] = dit["image"]
    dit_user_details['desp'] = dit["desp"]

    dit_user_details['dob'] = dit["dob"]
    dit_user_details['gender'] = dit["gender"]
    dit_user_details['passion'] = dit["passion"]
    dit_user_details['job'] = dit["job"]
    dit_user_details['company'] = dit["company"]

    dit_user_details['location'] = dit["location"]
    dit_user_details['createdAt'] = firestore.SERVER_TIMESTAMP

    store.collection("users").document(uid).set(dit_user_details)

    message = "User Data Updated"

    return jsonify({"Response": 200, "uid": uid, "message": message})

@app.route('/getFeed', methods=['POST'])
def getFeed(country):
    dit = request.get_json(force=True)
    docs= store.collection("users").where("gender","==",gender).stream()
    dit={}
    for doc in docs:
        if doc.to_dict().get("location").get("country")==country:
            dit[doc.id]=doc.to_dict()
    return dit

@app.route('/swipeFun', methods=['POST'])
def swipeFun(uidA, uidB, isA_Yes, isB_Yes):
    dit = request.get_json(force=True)
    dit={}
    dit["UID_A"]=uidA
    dit["UID_B"]=uidB
    dit["isUserA_Yes"]=isA_Yes
    dit["isUserB_Yes"]=isB_Yes
    dit["isTheOtherUserShownProfileAtLeastOnce"]=firstTime
    dit["createdAt"]=firestore.SERVER_TIMESTAMP

    store.collection("swipes").add(dit)

@app.route('/getMatchFun', methods=['POST'])
def getMatchFun(uid):
    dit = request.get_json(force=True)
    docs = store.collection("swipes").stream()
    ditSwipes = {}
    for doc in docs:
        if (doc.to_dict().get("UID_A") == uid or doc.to_dict().get("UID_B") == uid) and (doc.to_dict().get("isUserA_Yes") == True and doc.to_dict().get("isUserB_Yes") == True):
            ditSwipes[doc.id] = doc.to_dict()
    return ditSwipes


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=False)
