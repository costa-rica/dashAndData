import os
import pandas as pd
from datetime import date
from datetime import timedelta
import datetime
import requests
from requests.exceptions import MissingSchema
from flask import current_app
import numpy as np
from dashAndData import db
from dashAndData.models import Industrynames,Industryvalues, Commoditynames, Commodityvalues
from dashAndData.modelsCage import Cagecompanies
#added for BLS API call
from sqlalchemy import func
from dateutil.relativedelta import relativedelta
import json

def uploadToDfUtil(uploadFilename, uploadedFile):
    fileType=uploadFilename.rsplit('.', 1)[1].lower()
    if fileType == 'xlsx':
        dfUpload = pd.read_excel(uploadedFile,header=None)
    elif fileType == 'csv':
        dfUpload = pd.read_csv(uploadedFile,header=None)
    dfUpload.columns = ['Url List']
    return dfUpload


def textToDfUtil(uploadedText):
    urlList=uploadedText.split(',')
    urlList=[i.strip() for i in urlList]
    uploadDf =pd.DataFrame(urlList,columns=['Url List'])
    return uploadDf


def getStsUtil(website):
    try:
        v=requests.get(website)
        z=v.headers['Strict-Transport-Security']
        print('getStsUtil(website)::',z)
    except MissingSchema:
        z='no status found'
    except KeyError:
        z='no status found'
    except BaseException:
        #exception for InvalidURL (i.e. InvalidURL not an 'Exception'
        z='not a valid url'
    # except Exception:
        # print('Exception:::', Exception)
        # print(dir(Exception))
        # print('args:::::',Exception.args)
        # print('with_traceback:::',Exception.with_traceback)
        # z='not a url'

    return z



def toExcelUtility(file,sheetName, df):
    excelObj=pd.ExcelWriter(file,
        datetime_format='yyyy-mm-dd')
    workbook=excelObj.book
    sheetName=sheetName
    df.to_excel(excelObj,sheet_name=sheetName,index=False)
    worksheet=excelObj.sheets[sheetName]

    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'border': 0})
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value,header_format)
        width=len(value) if len(value)>10 else 10
        worksheet.set_column(col_num,col_num,width)
    
    return excelObj

def makeDfUtil(uploadDf):
    #remove any sts rows dates prior to yesterday
    houseFile = os.path.join(current_app.config['GET_STS_FILES'],'stsRecentHistory.xlsx')
    df=pd.read_excel(houseFile)
    
    yesterday = date.today() - timedelta(1)
    yesterday64 = np.datetime64(yesterday)
    houseDf = df[df['Date']>=yesterday64]

    #merge dfUpload into dfHouse
    houseDf=pd.merge(houseDf, uploadDf, on='Url List', how='outer')
    
    #filter all rows with no status -> dfNoStatus
    dfNoStatus=houseDf[houseDf.STS.isnull()]
    
    #Loop/request all no status rows update status column
    dfStatus=dfNoStatus.copy()
    dfStatus.reset_index(drop=True, inplace=True)

    for i in range(0,len(dfStatus)):
        dfStatus.at[i,'Date']=datetime.datetime.strftime(datetime.datetime.today(),'%m/%d/%Y')
        dfStatus.at[i,'STS']=getStsUtil(dfStatus.iloc[i,1])
    dfStatus.head()
    
    #Merge dfStatus into dfHouse
    houseDf.set_index('Url List', inplace=True)
    houseDf.update(dfStatus.set_index('Url List'))
    houseDf.reset_index(inplace=True)
    houseDf = houseDf[['Date','Url List','STS']].copy()
    
    #use merge only existing in dfUpload from dfHOuse i.e merge house into upload
    downloadDf=pd.merge(uploadDf,houseDf, how='left',on='Url List')
    downloadDf=downloadDf[['Date','Url List','STS']].copy()
    print('downloadDf::::',downloadDf)
    sheetName="STS Codes"
    excelObj= toExcelUtility(os.path.join(current_app.config['GET_STS_FILES'], 'stsRecentHistory.xlsx'),sheetName, houseDf)
    excelObj2= toExcelUtility(os.path.join(current_app.config['GET_STS_FILES'], 'STS Codes Report.xlsx'),sheetName, downloadDf)

    excelObj.close()
    excelObj2.close()




