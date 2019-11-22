# Dependencies
# ----------------------------------

import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

import psycopg2 as pg

import sys
import json
sys.path.append("..")

# Imports the methods needed to abstract classes into tables
from sqlalchemy.ext.declarative import declarative_base

# Allow us to declare column types
from sqlalchemy import Column, Integer, String, Float 

from flask_heroku import Heroku

app = Flask(__name__)




@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")




if __name__ == "__main__":
    app.run()
