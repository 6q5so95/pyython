#!/opt/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""finance情報をネットから取得してPostgresにロードする

"""
##########################################
# library
##########################################
import pandas as pd
import psycopg2
import sys

from datetime import datetime
from sqlalchemy import create_engine

##########################################
# param定義 TODO yaml
##########################################
# データベースの接続情報
connection_config = {
    'user': 'datamanager',
    'password': '5la&2Rj%4',
    'host': 'localhost',
    'port': '5433',
    'database': 'studydb'
}

# engin生成
engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(**connection_config))

##########################################
# app定義 TODO yaml
##########################################
# SIMBOL定義
SIMBOL_FRED = ['DFII10']
SIMBOL_YAHOO_FINANCE = [
        '^NDX', # NASDAQ100
        'SOXL', # SOX BULL☓3
        'vED',  # エネルギー
        'VPD',  # 公共事業
        'VDC',  # 生活必需品
        'VFH',  # 金融
        'VAW',  # 素材
        'VHT',  # ヘルスケア
        'VIS',  # 資本財    
        'VCR',  # 一般消費材
        'VGT',  # 情報技術
        'VOX',  # コミュニケーション
        'VNQ',  # 不動産
        ]

# 日付定義
START_DATE_YYYYMMDD = '2003-01-01'
START_DATE_UNIXTIME = '1041379200'
TODAY_YYYYMMDD = datetime.now().strftime('%Y-%m-%d')
TODAY_UNIXTIME = int(datetime.now().timestamp())


##########################################
# 関数定義
##########################################

def getFredUrl(simbol: str) -> str:
    return f'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id={simbol}&scale=left&cosd={START_DATE_YYYYMMDD}&coed={TODAY_YYYYMMDD}&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Daily&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2022-04-29&revision_date=2022-04-29&nd=2003-01-02'

def getYahooFinanceUrl(simbol: str) -> str:
    return f'https://query1.finance.yahoo.com/v7/finance/download/{simbol}?period1={START_DATE_UNIXTIME}&period2={TODAY_UNIXTIME}&interval=1d&events=history&includeAdjustedClose=true'

def getFredData() -> dict:
    # dictに格納
    _dfs = {}

    # Data取得
    for _SIMBOL in SIMBOL_FRED:
        FILE_PATH_FRED = getFredUrl(_SIMBOL)
        try:
            df = pd.read_csv(
                    FILE_PATH_FRED,
                    parse_dates=['DATE'],
                    )
        except Exception as e:
            print(f'FREDからのデータ取得に失敗しました')
            print(f'Error: {e}')
            sys.exit(1)

        # EDA
        ## データを持たない場合は . が設定されているのでこれを取り除く
        df = df[df[_SIMBOL] != '.']
        df[_SIMBOL] = df[_SIMBOL].astype('float64')

        # データ積み上げ
        _dfs[_SIMBOL] = df

    return _dfs

def getYahooFinanceData() -> dict:
    # dictに格納
    _dfs = {}

    # Data取得
    for _SIMBOL in SIMBOL_YAHOO_FINANCE:
        FILE_PATH_YAHOO_FINANCE = getYahooFinanceUrl(_SIMBOL)
        try:
            df = pd.read_csv(
                    FILE_PATH_YAHOO_FINANCE,
                    parse_dates=['Date'],
                    )
        except Exception as e:
            print(f'Yahoo Financeからのデータ取得に失敗しました')
            print(f'Error: {e}')
            sys.exit(1)

        # EDA
        ## 終値のみで評価する
        df = df[['Date', 'Close']]

        # データ積み上げ
        _dfs[_SIMBOL] = df

    return _dfs

def loadFinanceDataToPostgres(dfs: dict) -> None:

    # Postgresは小文字でテーブル作成が必要
    for _SIMBOL, _df in dfs.items():
        SIMBOL = _SIMBOL.lower().replace('^','')
        try:
            _df.to_sql(SIMBOL, con=engine, if_exists='replace', index=False)
        except Exception as e:
            print(f'Postgresへのデータロードに失敗しました')
            print(f'Error: {e}')
            sys.exit(1)
        print(f'SIMBOL: {SIMBOL}')

##########################################
# main 
##########################################
def main():
    # Fredデータ処理
    dfs = getFredData()
    loadFinanceDataToPostgres(dfs)

    # Yahoo Finance処理
    dfs = getYahooFinanceData()
    loadFinanceDataToPostgres(dfs)

##########################################
# 起動 
##########################################
if __name__ == '__main__':
    main()

                        
