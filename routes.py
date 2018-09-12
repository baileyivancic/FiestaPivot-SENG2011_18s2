from flask import Flask, redirect, render_template, request, url_for, flash, request, Response
from flask_login import UserMixin
from flask_login import LoginManager,login_user, current_user, login_required, logout_user
import json
from server import app, login_manager


@app.route('/',  methods=["GET", "POST"])
def landing_page():
    return render_template("register.html")