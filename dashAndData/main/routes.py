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
import smtplib
# from email.mime.text import MIMEText
# from email.MIMEMultipart import MIMEMultipart
from email.message import EmailMessage

main = Blueprint('main', __name__)


@main.route("/", methods=["GET","POST"])
@main.route("/home", methods=["GET","POST"])
def home():
    if request.method == 'POST':
        formDict = request.form.to_dict()
        # Corey Shafer email tutorial: https://www.youtube.com/watch?v=JRCJ6RtE3xU

        email_submit=formDict.get('email')
        message_submit=formDict.get('message')
        name_submit=formDict.get('name')
        
#confirmation email
        msg_conf = EmailMessage()
        msg_conf['Subject'] = 'Message Sent to Dashboards and Databases'
        msg_conf['From'] = current_app.config['MAIL_USERNAME_TGE']
        msg_conf['To'] = email_submit
        msg_conf.add_alternative(f"""\
<!DOCTYPE html>
<html>
    <body>
        <h3 style="color:SlateGray;">Dashboards and Databases</h3><br/>
        This is a confirmation that your email was sent.<br/>
        Name: {name_submit}<br/>
        Message: {message_submit}
    </body>
</html>
""", subtype='html')
        with smtplib.SMTP(current_app.config['MAIL_SERVER_GD'], current_app.config['MAIL_PORT_GD']) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(current_app.config['MAIL_USERNAME_TGE'],current_app.config['MAIL_PASSWORD_TGE'])
            smtp.send_message(msg_conf)

#notification email
        msg_from_DandD = EmailMessage()
        msg_from_DandD['Subject'] = 'Message from Dashboards and Databases'
        msg_from_DandD['From'] = current_app.config['MAIL_USERNAME_TGE']
        msg_from_DandD['To'] = current_app.config['MAIL_USERNAME_TGE']
        msg_from_DandD.add_alternative(f"""\
<!DOCTYPE html>
<html>
    <body>
        <h3 style="color:SlateGray;">Dashboards and Databases</h3><br/>
        Name: {name_submit}<br/>
        Email: {email_submit}<br/>
        Message: {message_submit}
    </body>
</html>
""", subtype='html')
        with smtplib.SMTP(current_app.config['MAIL_SERVER_GD'], current_app.config['MAIL_PORT_GD']) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(current_app.config['MAIL_USERNAME_TGE'],current_app.config['MAIL_PASSWORD_TGE'])
            smtp.send_message(msg_from_DandD)

        
        print('Mail Sent!, Success!')
        flash('Message Sent!', 'success')
        redirect(url_for('main.home')+'#contactModal')
        return redirect(url_for('main.home', _anchor="contact_section_id"))
        
        # return redirect(url_for('main.home')+'#contactModal')
    return render_template('index.html')







