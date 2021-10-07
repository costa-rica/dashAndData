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

from dashAndData.datatools.blsSearch.utils import checkStatusUtility, \
    formatSeriesIdListUtil, seriesIdTitleListIndustry, seriesIdTitleListCommodity, \
    priceIndicesToDf,buildMetaDfUtil,makeExcelObj_priceindices,annualizeDf, \
    quarterizeDf,makeSearchExactDict, updateDbWithApi


datatools_bls = Blueprint('datatools_bls', __name__,url_prefix='/datatools_bls')

    
@datatools_bls.route('/bls_data_menu',methods=['POST','GET'])
def bls_menu():
    return render_template("bls_data_menu.html")


@datatools_bls.route('/blsIndustry',methods=['POST','GET'])
def blsIndustry():
    #Delete download file if exists
    if os.path.exists(os.path.join(current_app.static_folder, 'blsIndustry','blsIndustryPPI.xlsx')):
        os.remove(os.path.join(current_app.static_folder, 'blsIndustry','blsIndustryPPI.xlsx'))
    siteTitle = "BLS Industry Producer Price Index (PPI)"
    session['textareaEntry'] = request.args.get('textareaEntry_new')
    cs0=request.args.get('cs0')
    cs1=request.args.get('cs1')
    cs2=request.args.get('cs2')
    cs3=request.args.get('cs3')
    cs4=request.args.get('cs4')
    cs5=request.args.get('cs5')
    cs6=request.args.get('cs6')
    cs7=request.args.get('cs7')
    cs8=request.args.get('cs8')
    cs9=request.args.get('cs9')
    cs10=request.args.get('cs10')
    cs11=request.args.get('cs11')
    cs12=request.args.get('cs12')
    cs13=request.args.get('cs13')
    colNames=['series_id','series_title']
    indexSeriesIdTitleList=seriesIdTitleListIndustry()

    if request.method=="POST":
        formDict = request.form.to_dict()
        textareaEntry_new=formDict.get('textareaEntry')
        addSeries_id=formDict.get('addSeries_id')
        periodicity = formDict.get('periodicty')
        print('formDict:::',formDict)
        

        if addSeries_id:
            csUtil = checkStatusUtility(formDict)
            if textareaEntry_new != None and textareaEntry_new != "":
                textareaEntry_new = textareaEntry_new + ',\n' + addSeries_id
            else:
                textareaEntry_new = addSeries_id 
            return redirect(url_for('datatools_bls.blsIndustry', textareaEntry_new=textareaEntry_new, cs0=csUtil[0],
                cs1=csUtil[1],cs2=csUtil[2],cs3=csUtil[3],cs4=csUtil[4],cs5=csUtil[5],cs6=csUtil[6],cs7=csUtil[7],
                cs8=csUtil[8],cs9=csUtil[9],cs10=csUtil[10], cs11=csUtil[11],cs12=csUtil[12],cs13=csUtil[13]))

        elif formDict.get('downloadButton') and textareaEntry_new != '':
            seriesIdList=session['textareaEntry'].replace('\r\n','')
            #make seriesId for db/api check and indexValuesDf
            seriesIdListClean=formatSeriesIdListUtil(seriesIdList)
            print('Series Requested: ',seriesIdListClean)
            
            updateDbWithApi(seriesIdListClean, 'industryvalues')#<---checks db for requested data not current
            #if any requested data is not of a month 2 months and 13 days from the current date then api call
            
            indexValuesDf=priceIndicesToDf(seriesIdListClean,'Industry')

            #make list for meta data
            metaDataItemsList=[i[:-8] for i in formDict.keys() if 'Checkbox' in i]

            #use list to make metadata indexValuesDf
            metaDf = buildMetaDfUtil(seriesIdListClean, metaDataItemsList, 'Industry')

            #create ExcelWriter object with date formatted, col heading formatted and values centered
            filePathAndName=os.path.join(current_app.config['BLS'],'blsIndustryPPI.xlsx')
            sheetName='Indices'

            excelObj=makeExcelObj_priceindices(filePathAndName,metaDf,indexValuesDf,seriesIdListClean,
                metaDataItemsList,sheetName, periodicity)
            excelObj.close()
            return send_from_directory(os.path.join(current_app.config['BLS']),'blsIndustryPPI.xlsx', as_attachment=True)

            
        elif formDict.get('clearButton'):
            if os.path.exists(os.path.join(current_app.config['BLS'],'blsIndustryPPI.xlsx')):
              os.remove(os.path.join(current_app.config['BLS'],'blsIndustryPPI.xlsx'))

            return redirect(url_for('datatools_bls.blsIndustry', cs11="checked"))
        else:
            flash(f'No indices requested', 'warning')
            return redirect(url_for('datatools_bls.blsIndustry'))
            
    return render_template('blsIndustry.html', siteTitle=siteTitle, indexSeriesIdTitleList=indexSeriesIdTitleList,
    colNames=colNames, len=len, str=str, textareaEntry=session['textareaEntry'], cs0=cs0,
                cs1=cs1,cs2=cs2,cs3=cs3,cs4=cs4,cs5=cs5,cs6=cs6,cs7=cs7,cs8=cs8,cs9=cs9,cs10=cs10,cs11=cs11,
                cs12=cs12,cs13=cs13)



@datatools_bls.route('/blsCommodity',methods=['POST','GET'])
def blsCommodity():
    #Delete download file if exists
    if os.path.exists(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx')):
        os.remove(os.path.join(current_app.static_folder, 'blsCommodity','blsCommodityPPI.xlsx'))
    siteTitle='BLS Commodity Producer Price Index (PPI)'
    session['textareaEntry'] = request.args.get('textareaEntry_new')
    cs0=request.args.get('cs0')
    cs1=request.args.get('cs1')
    cs2=request.args.get('cs2')
    cs3=request.args.get('cs3')
    cs4=request.args.get('cs4')
    cs5=request.args.get('cs5')
    cs6=request.args.get('cs6')
    cs7=request.args.get('cs7')
    cs8=request.args.get('cs8')
    cs9=request.args.get('cs9')
    cs10=request.args.get('cs10')
    cs11=request.args.get('cs11')
    cs12=request.args.get('cs12')
    cs13=request.args.get('cs13')
    colNames=['series_id','series_title']
    indexSeriesIdTitleList=seriesIdTitleListCommodity()
    
    if request.method=="POST":
        formDict = request.form.to_dict()
        textareaEntry_new=formDict.get('textareaEntry')
        addSeries_id=formDict.get('addSeries_id')
        periodicity = formDict.get('periodicty')

        if addSeries_id:
            csUtil = checkStatusUtility(formDict)
            if textareaEntry_new != None and textareaEntry_new != "":
                textareaEntry_new = textareaEntry_new + ',\n' + addSeries_id
            else:
                textareaEntry_new = addSeries_id 
            return redirect(url_for('datatools_bls.blsCommodity', textareaEntry_new=textareaEntry_new, cs0=csUtil[0],
                cs1=csUtil[1],cs2=csUtil[2],cs3=csUtil[3],cs4=csUtil[4],cs5=csUtil[5],cs6=csUtil[6],cs7=csUtil[7],
                cs8=csUtil[8],cs9=csUtil[9],cs10=csUtil[10], cs11=csUtil[11],cs12=csUtil[12],cs13=csUtil[13]))

        elif formDict.get('downloadButton') and textareaEntry_new != '':
            seriesIdList=session['textareaEntry'].replace('\r\n','')
            #make seriesId for indexValuesDf
            seriesIdListClean=formatSeriesIdListUtil(seriesIdList)
            print(seriesIdListClean)
            indexValuesDf=priceIndicesToDf(seriesIdListClean,'Commodity')

            updateDbWithApi(seriesIdListClean, 'commodityvalues')#<---checks db for requested data not current
            #if any requested data is not of a month 2 months and 13 days from the current date then api call
            
            indexValuesDf=priceIndicesToDf(seriesIdListClean,'Commodity')

            #make list for meta data
            metaDataItemsList=[i[:-8] for i in formDict.keys() if 'Checkbox' in i]
            print('metaDataItemsList:::',metaDataItemsList)

            #use list to make metadata indexValuesDf
            metaDf = buildMetaDfUtil(seriesIdListClean, metaDataItemsList, 'Commodity')

            #create ExcelWriter object with date formatted, col heading formatted and values centered
            filePathAndName=os.path.join(os.path.join(current_app.config['BLS'],'blsCommodityPPI.xlsx'))
            sheetName='Indices'
            #if annualize
            excelObj=makeExcelObj_priceindices(filePathAndName,metaDf,indexValuesDf,seriesIdListClean,
                metaDataItemsList,sheetName, periodicity)
            excelObj.close()
            return send_from_directory(current_app.config['BLS'],'blsCommodityPPI.xlsx', as_attachment=True)

            
        elif formDict.get('clearButton'):
            if os.path.exists(os.path.join(current_app.config['BLS'],'blsCommodityPPI.xlsx')):
              os.remove(os.path.join(current_app.config['BLS'],'blsCommodityPPI.xlsx'))

            return redirect(url_for('datatools_bls.blsCommodity', cs11="checked"))
        else:
            flash(f'No indices requested', 'warning')
            return redirect(url_for('datatools_bls.blsCommodity'))
            
            
    return render_template('blsCommodity.html', siteTitle=siteTitle, indexSeriesIdTitleList=indexSeriesIdTitleList,
        colNames=colNames, len=len, str=str, textareaEntry=session['textareaEntry'], cs0=cs0,
        cs1=cs1,cs2=cs2,cs3=cs3,cs4=cs4,cs5=cs5,cs6=cs6,cs7=cs7,cs8=cs8,cs9=cs9,cs10=cs10,cs11=cs11,
        cs12=cs12,cs13=cs13)


