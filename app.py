from flask import Flask, request, abort, render_template, redirect, url_for, jsonify, flash
from firebase_admin import firestore, initialize_app, credentials
import os
import json

# Firebaseの初期化
cred_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)
initialize_app(cred)


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)