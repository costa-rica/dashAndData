from flask import Blueprint

from flask import render_template, url_for, redirect, flash, request, abort, session,\
    Response, current_app, send_from_directory
# from dashAndData import db
# from dashAndData.models import Datatools
import os
# from datetime import datetime, date, time
# from sqlalchemy import func
# import pandas as pd
# import xlsxwriter
# import openpyxl
# import json

from dashAndData.datatools.cage_search.utils import makeSearchExactDict, \
    searchQueryCageToDf, cageExcelObjUtil


datatools_cage = Blueprint('datatools_cage', __name__,url_prefix='/datatools_cage')

    
@datatools_cage.route('/cageCodeSearch',methods=['POST','GET'])
def cageCodeSearch():
    #Delete download file if exists
    # if os.path.exists(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx')):
        # os.remove(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx'))
    siteTitle='CAGE Code Lookup'
    searchDictClean={'companyName':'Company Name', 'companyNameSub':'Company Name (Subsidiary)','cageCode': 'CAGE Code',
        'address': 'Address', 'city': 'City', 'state': 'State'}
    if request.method=="POST":
        formDict = request.form.to_dict()
        if formDict.get('clearButton'):
            return redirect(url_for('datatools_cage.cageCodeSearch'))

        searchStringDict,exactDict = makeSearchExactDict(formDict)
        #re-Key searchStringDict for webpage
        searchDictClean={'companyName':'Company Name', 'companyNameSub':'Company Name (Subsidiary)','cageCode': 'CAGE Code',
            'address': 'Address', 'city': 'City', 'state': 'State'}
        searchStringDict={searchDictClean[i]:j for i,j in searchStringDict.items()}
        exactDict={searchDictClean[i]:j for i,j in exactDict.items()}
        
        count=0
        for i in searchStringDict.values():
            count=count + len(i)
        if count<2:
            flash(f'Query too broad. Must enter at least two search characters to narrow search.', 'warning')
            return redirect(url_for('datatools.cageCodeSearch'))

        df=searchQueryCageToDf(formDict)
        resultsCount = len(df)
        if resultsCount>10000:
            flash(f'Query beyond 10,000 row limit. Must enter more search criteria to narrow search.', 'warning')
            return redirect(url_for('datatools.cageCodeSearch'))
        if formDict.get('searchCage')=='search':
            columnNames = df.columns
            dfResults = df.to_dict('records')
            print('searchStringDict:::',searchStringDict)
            
            return render_template('cageCodeSearch.html', siteTitle=siteTitle, columnNames=columnNames, dfResults=dfResults,
                len=len, searchStringDict=searchStringDict, exactDict=exactDict, searchDictClean=searchDictClean,
                resultsCount='{:,}'.format(resultsCount))
        if formDict.get('searchCage')=='download':
            filePathAndName=os.path.join(current_app.static_folder, 'cageSearch','CAGE_SearchResults.xlsx')
            excelObj=cageExcelObjUtil(filePathAndName,df)
            excelObj.close()
            return send_from_directory(os.path.join(current_app.static_folder, 'cageSearch'),'CAGE_SearchResults.xlsx', as_attachment=True)
    return render_template('cageCodeSearch.html', siteTitle=siteTitle, searchDictClean=searchDictClean)
