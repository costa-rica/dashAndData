from flask import Blueprint

from flask import render_template, url_for, redirect, flash, request, abort, session,\
    Response, current_app, send_from_directory
# from dashAndData import db
# from dashAndData.models import Datatools
import os
from datetime import datetime, date, time
# from sqlalchemy import func
import pandas as pd
# import xlsxwriter
# import openpyxl
# import json

from dashAndData.datatools.security.utils import uploadToDfUtil, \
    textToDfUtil, getStsUtil,toExcelUtility,makeDfUtil


datatools_security = Blueprint('datatools_security', __name__,url_prefix='/datatools_security')

 
@datatools_security.route("/", methods=['POST','GET'])
# @datatools.route("/getSTS", methods=['POST','GET'])
def getSTS():
    siteTitle = "Get STS Codes"
    today = date.today().strftime("%m/%d/%Y")
    
    if request.args.get('goToPriceIndices'):
        return redirect(url_for('datatools.priceIndices', goTo=request.args.get('goToPriceIndices')))
    
    if request.method=="POST":
        formDict = request.form.to_dict()
        filesDict = request.files.to_dict()
        
        uploadFilename = filesDict.get('uploadedFile').filename
        uploadedText = formDict.get('textareaEntry')
        
        #check file data upload type
        #make df from data upload
        if uploadFilename:
            uploadedFile = request.files['uploadedFile']
            if '.' in uploadFilename and uploadFilename.rsplit('.', 1)[1].lower() in ['xlsx', 'csv']:
                uploadDf=uploadToDfUtil(uploadFilename, uploadedFile)
            else:
                flash(f'File not accepted ', 'warning')
                return redirect(url_for('datatools.getSTS'))
        elif uploadedText:
            uploadDf=textToDfUtil(uploadedText)
        else:
            flash(f'No web addresses provided. Enter url in text box or upload spreadsheet', 'warning')
            return redirect(url_for('datatools.getSTS'))
        
        makeDfUtil(uploadDf)
            
        if formDict.get('button') == 'makeTable':
            stsTable = pd.read_excel(os.path.join(current_app.config['GET_STS_FILES'], 'STS Codes Report.xlsx'))
            stsTable['Date']=stsTable['Date'].dt.date
            stsTableColumns = stsTable.columns
            stsTable=stsTable.to_dict('records')
            return render_template("getSts.html", siteTitle = siteTitle,stsTable=stsTable, stsTableColumns=stsTableColumns, len=len)       

        elif formDict.get('button') == 'downloadTable':
            return send_from_directory(os.path.join(current_app.root_path, 'static','getSts'),'STS Codes Report.xlsx', as_attachment=True)
            
        # return render_template("getSts.html")
    return render_template("getSts.html", siteTitle = siteTitle, len=len)
