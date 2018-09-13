import flask_login
from flask import Flask, redirect, render_template, request, url_for, flash, request, Response
from flask_login import UserMixin
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
import json
from database import Database
from server import app, login_manager


@app.route('/',  methods=["GET", "POST"])
def index():
    return render_template("index.html")
