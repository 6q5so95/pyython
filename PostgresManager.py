import psycopg2
import sys
from sqlalchemy import create_engine

class PostgresManager:
    def __init__(self, **connParam):
        self._connParam = connParam
    
    def createEngine(self):
        # param check
        #print(self._connParam)

        # engine パラメータ生成
        engineString = f"postgresql://{self._connParam['user']}:'{self._connParam['password']}'@{self._connParam['host']}:{self._connParam['port']}/{self._connParam['database']}"
        #print(engineString)

        # engine 生成
        try:
            engine = create_engine(f"{engineString}".format(**self._connParam), echo=True)
        except Exception as e:
            print('Postgres接続に失敗しました')
            print(f'err: {e}')
            sys.exit(1)
        
        return engine

def main():    
    # 使い方    
    connection_config = {
        'user': 'postgres',
        'password': 'xxxxxxxxxxxxxxxx',
        'host': 'localhost',
        'port': 'xxxx',
        'database': 'xxxxxx'
    }

    # インスタンス生成
    postgres = PostgresManager(**connection_config)

    # engine取得
    engine = postgres.createEngine()

    # dataframeからPostgresへデータロード（例）
    data.to_sql('apachelog', con=engine, if_exists='replace', index=False)

# 起動
if __name__ == '__main__':
    main()
    


    
    
    
   
    
    
