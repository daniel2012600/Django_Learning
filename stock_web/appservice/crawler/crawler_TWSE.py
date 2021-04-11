# 取得台股日線資料與高頻資料
import os 
import arrow
import io
import re
import numpy as np
import requests
import pandas as pd
import json
import matplotlib.pyplot as pp
import time
import pymysql
import json
import logging
MYSQL_HOST = 'localhost'
MYSQL_DB = 'twstock'
MYSQL_USER = 'root'
MYSQL_PASS = 'root'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
#   http://www.twse.com.tw/exchangeReport/STOCK_DAY?date=20180817&stockNo=2330

def connect_mysql():  #連線資料庫
    global connect, cursor
    connect = pymysql.connect(host = MYSQL_HOST, db = MYSQL_DB, user = MYSQL_USER, password = MYSQL_PASS,
            charset = 'utf8', use_unicode = True)
    cursor = connect.cursor()


# date_time = YYYYMMDD
def crawler(date_time):
    page_url = f'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date={date_time}&type=ALLBUT0999'
    page = requests.get(page_url)
    use_text = page.text.splitlines()
    for index, text in enumerate(use_text):
        if text == '"證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比",':
            initital_point = index
            break
    test_df = pd.read_csv(io.StringIO(''.join([text[:-1] + '\n' for text in use_text[initital_point:]])))
    test_df['證券代號'] = test_df['證券代號'].apply(lambda x:x.replace('=',''))
    test_df['證券代號'] = test_df['證券代號'].apply(lambda x:x.replace('"',''))
    return test_df


def parse_n_days(start_date, n):
    df_dict = {}
    now_date = start_date
    for index in range(n):
        time.sleep(3)
        now_date = now_date.shift(days=-1)
        try:
            crawler_date = now_date.format("YYYYMMDD")
            df = crawler(crawler_date)
            logger.info('Successful!!' + ' ' + crawler_date)
            df_dict.update({crawler_date:df})
        except:
            logger.info('Falls at' + ' ' + crawler_date)
    return df_dict

# ============================= shares 成交股數 ===========================

# t = arrow.now()
# my_result = parse_n_days(t,4)
# for key in my_result.keys():
#     # 檢查檔案是否存在
#     filepath = f'./stock_data/{str(key)}.csv'
#     if os.path.isfile(filepath):
#         print("檔案存在。")
#     else:
#         print("檔案不存在。")
#         my_result[key].to_csv(filepath)
connect_mysql()
# my_qry = 'SELECT * FROM stock.twse;'
# cursor.execute(my_qry)
# myresult = cursor.fetchall()

# for x in myresult:
#   print(x)
# qmarks = ', '.join(f'{len(my_result)}')
# qry = "Insert Into Table (%s) Values (%s)" % (qmarks, qmarks)
# cursor.execute(qry, my_result.keys() + my_result.values())

# for file_name in All_csv_file:
#     pd.read_csv(file_name).iloc[:,1:].to_sql(file_name.replace('.csv',''),db,if_exists='replace')
# df.to_sql(key,db2,if_exists='replace')

# # **金融分析日記 EP2 - 將抓到的資料整理成資料庫**
import pandas as pd
import sqlite3
import glob

# '''
# glob套件是用來查找符合特定規則的文件名，跟我們用搜尋跳出來的結果差不多，這邊我們查詢副檔名為csv的檔案並存為一個列表的形式。
# '''
All_csv_file = glob.glob('20210409.csv')
print(All_csv_file)
# df = pd.read_csv(All_csv_file[0]).iloc[:,1:]
# print(df)


# '''
# # 此內容會顯示為程式碼


# ## 第二部份 創建資料庫，存成以時間為一張張表的資料庫
# 我們這邊會使用sqlite來存取我們抓下來的股價資料
# - python內建sqlite套件，我們無須特安裝
# - 支援完整sql語法查詢我們的資料
# - 使用以及轉移方便，一個資料庫就像一個本地文件一樣

# 在這邊，我們直接使用DataFrame提供把DataFrame存入Sql資料庫當作表格的方法。
# '''


# dbname = 'TWStock.db'
# #連接到我們的資料庫，如果沒有的話會重新建一個
# db = sqlite3.connect(dbname)
# for file_name in All_csv_file:
#     pd.read_csv(file_name).iloc[:,1:].to_sql(file_name.replace('.csv',''),db,if_exists='replace')


# ### 如何讀取資料庫的表格
# # 我們這邊簡單介紹如何讀取sqlite檔案裡面的表格

# dates_list = [file_name.replace('.csv','') for file_name in All_csv_file]

# pd.read_sql(con=db,sql='SELECT * FROM' + ' "'+ dates_list[0] +'"').head()


# total_df = pd.DataFrame()
# for date in dates_list:
#     df = pd.read_sql(con=db,sql='SELECT * FROM' + ' "'+ date +'"')
#     df['Date'] = date
#     total_df = total_df.append(df)

# dbname_2 = 'TWStock_2'
# db2 = sqlite3.connect(dbname_2)
# total_dict = dict(tuple(total_df.groupby('證券代號')))
# for key in total_dict.keys():
#     df = total_dict[key].iloc[:,2:]
#     df['Date'] = pd.to_datetime(df['Date'])
#     df = df.sort_values(by=['Date'])
#     df.to_sql(key,db2,if_exists='replace')


# print(pd.read_sql(con=db2,sql='SELECT * FROM "2330"').tail())

# # **金融分析日記 EP3 -股票收益率與風險評估**

# # 載入套件庫並讀入資料
# import pandas as pd
# import matplotlib.pyplot as plt
# import sqlite3
# import numpy as np

# db = sqlite3.connect('TWStock_2')
# #這邊我們挑選一些台灣的代表性股票
# stocks_dict = {}
# #台積電2330
# stocks_dict.update({'tsmc':pd.read_sql(con=db,sql='SELECT * FROM "2330"')})
# #台塑化6505
# stocks_dict.update({'fpc':pd.read_sql(con=db,sql='SELECT * FROM "6505"')})
# #鴻海2317
# stocks_dict.update({'foxconn':pd.read_sql(con=db,sql='SELECT * FROM "2317"')})
# #中華電2412
# stocks_dict.update({'cht':pd.read_sql(con=db,sql='SELECT * FROM "2412"')})
# #台塑1301
# stocks_dict.update({'fpg':pd.read_sql(con=db,sql='SELECT * FROM "1301"')})
# #台化1326
# stocks_dict.update({'fcfc':pd.read_sql(con=db,sql='SELECT * FROM "1326"')})
# #國泰金2882
# stocks_dict.update({'cfh':pd.read_sql(con=db,sql='SELECT * FROM "2882"')})
# #南亞1303
# stocks_dict.update({'ny':pd.read_sql(con=db,sql='SELECT * FROM "1303"')})
# #富邦金2881
# stocks_dict.update({'fubon':pd.read_sql(con=db,sql='SELECT * FROM "2881"')})
# #大立光3008
# stocks_dict.update({'largan':pd.read_sql(con=db,sql='SELECT * FROM "3008"')})

# # 繪製基本股價走勢圖
# # 我們在這邊先繪製這幾隻股票的收盤價的走勢圖

# '''
# 在畫圖之前，
# 我們先整理我們的資料，將每個股票整理成股票名稱與收盤價的表格形式，
# 其中，因為收盤價被存為字串形式，我們也必須轉為數值形式做進一個的運算
# '''
# for key in stocks_dict.keys():
#     df = stocks_dict[key]
#     df.index = df['Date']
#     df.index = pd.to_datetime(df.index)
#     df = df[['證券名稱','收盤價']]
#     df['收盤價'] = pd.to_numeric(df['收盤價'].apply(lambda x:x.replace(',','')),errors='coerce')
#     df.columns = ['stock_code','close']
#     stocks_dict[key] = df


# fig,ax = plt.subplots(3,2,figsize=(10,10))
# plt.subplots_adjust(hspace=0.8)
# stocks_dict['largan']['2021-01-01':].plot(ax=ax[0,0])
# ax[0,0].set_title('Largan')
# stocks_dict['tsmc']['2021-01-01':].plot(ax=ax[0,1])
# ax[0,1].set_title('TSMC')
# stocks_dict['fubon']['2021-01-01':].plot(ax=ax[1,0])
# ax[1,0].set_title('Fubon')
# stocks_dict['cfh']['2021-01-01':].plot(ax=ax[1,1])
# ax[1,1].set_title('CFH')
# stocks_dict['fpg']['2021-01-01':].plot(ax=ax[2,0])
# ax[2,0].set_title('FPG')
# stocks_dict['fpc']['2021-01-01':].plot(ax=ax[2,1])
# ax[2,1].set_title('FPC')
# fig.suptitle('Stock Price via time')
# plt.show()


# df = stocks_dict['tsmc'].copy()
# df_p = df['2018-01-01':].iloc[:-1,:]
# df_a = df['2018-01-01':].iloc[1:,:]
# plt.scatter(np.array(df_p['close']), np.array(df_a['close']))
# plt.show
# plt.hist( [np.array(df['2018-01-01':]['close']), np.array(df['2018-09-01':]['close'])])







# -*- coding: utf-8 -*-
class Config(object):

    SQL_CONFIG = {
        'host': '35.200.15.129',
        'connect_timeout': 60,
        'read_timeout': 60,
        'write_timeout': 60,
        'max_allowed_packet': 102400,
        'user': 'cdpdev',
        'password': 'cdp!@#',
        'db': 'cdpplatformdb',
        'charset': 'utf8mb4'
    }

    GCS_JSONKEY = 'static/json/KeywordTag-3c600346e709.json'
    DOWNLOAD_PATH = 'static/filedownload/'

    BQGCS_CONFIG = {
        'GCS_ACCESS_KEY': "GOOGT3VSRBINAZUOKSNFLDIL",
        'GCS_SECRET_KEY': "nl/3xDx2rrtiqswJJIrALnWsI4h/PoC7i9Wyr0Sl",
        'GCS_BUCKET_NAME': "cdpplatform_rule_result",
        'BQ_PROJECT_ID': "keywordtag",
        'BQ_SERVICE_ACCOUNT': "dmplogstore@keywordtag.iam.gserviceaccount.com",
        'BQ_PRIVATE_KEY_PATH': "static/json/KeywordTag-3c600346e709.json",
        'BQ_DEFAULT_QUERY_TIMEOUT': 86400,  # 24 hours
        'BQ_DEFAULT_EXPORT_TIMEOUT': 86400,  # 24 hours
    }

    MONGO_CONN_DB = 'cdpbackenddb'
    MONGO_CONN = "mongodb://savebar1122:s%40veb%40r0524@35.200.1.235:27017/"

    MAIL_CONFIG = {
        'EMAIL_SENDER': 'service@eagleeye.com.tw',
        'SEND_GRID_KEY': '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',
        'SEND_IN_BLUE_SENDER': {"name":"service", "email":"service@eagleeye.com.tw"},
        'SEND_IN_BLUE_KEY': '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',
    }

    CRYPTO_PWD = 'cdpweb'

    API_PRIVATE_KEY = '~st@)2{G\\4,~s7{4<Q<pvr8kWH+8=!Cv'

    CDP_BACKEND_WEB_URI = 'http://34.84.221.26:8800'


class ProdConfig(Config):
    ENV_NAME = "Production"
    KEY = 'app-key-in-config'
    WEB_URI = 'https://cdppj.eagleeye.com.tw'

class DevConfig(Config):
    ENV_NAME = "Develop"
    DEBUG = True
    WEB_URI = 'https://cdppj-sit.eagleeye.com.tw'
    # WEB_URI = 'http://127.0.0.1:5000'
