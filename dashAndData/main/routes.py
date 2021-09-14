from flask import Blueprint

from flask import render_template, url_for, redirect, flash, request, abort, session,\
    Response, current_app, send_from_directory
# from dashAndData import db
# from dashAndData.models import Datatools
import os
from datetime import datetime, date, time
from sqlalchemy import func
import pandas as pd
import xlsxwriter
import openpyxl
import json

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():

    return render_template('index.html')







