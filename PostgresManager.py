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
            engine = create_engine(f"{engineString}".format(**self._connParam))
        except Exception as e:
            print('Postgres接続に失敗しました')
            print(f'err: {e}')
            sys.exit(1)
        
        return engine
