from datetime import datetime
from datetime import timedelta
import numpy as np
from typing import Tuple

class CalcHotSpot:
    """HotSpot計算に必要となるit値を算出する
        修正が行われた時点のタイムスタンプでコードが生成されたときを0、現在を1と置いてその間の少数値をとります。
        つまり、12月1日にコードを書き始め、今日が12月30日であるとすると、15日にバグフィクスをしたらti=0.5になります。
        
    """    
    
    def __init__(self, start_hotspot_day):
        self.start_hotspot_day = start_hotspot_day
    
    
    def _CalcTimeInterval(self, update_day: datetime) -> float:
        """
        Args:
            HopSpot測定開始基準日 (datetime)
        Returns:
            float : it算出結果
        Raises:
            例外の名前: 例外の説明 (例 : 引数が指定されていない場合に発生 )
        Examples:
            >>> self_calcTimeInterval (hotspot_start_day)
        Note:
            datetime.datetime及びdatetime.timedeltaのimport
                >> from datetime import datetime
                >> from datetime import timedalta
        """    
        
        # 本日日付情報
        NOW = datetime.now()
    
        # ti値を算出
        return  float((update_day - self.start_hotspot_day + timedelta(days=1)).days) / \
                float((NOW - self.start_hotspot_day + timedelta(days=1)).days)
    
    
    def CalcHotSpotValue(self, updateDays:datetime) -> Tuple[float, float]:
        """
        Args:
            HopSpot測定対象日 (datetime)
        Returns:
            float, float: ti値、hs値
        Raises:
            例外の名前: 例外の説明 (例 : 引数が指定されていない場合に発生 )
        Examples:
            >> hotspot = CalcHotSpot(HOTSPOT_STARTDATE)
            >> for _ in LIST_UPDATE_DATES:
            >>    ti, hs = hotspot.CalcHotSpotValue(_)
            >>    print(f'ti = {ti:9.05} hs = {hs:9.05f}')
        See:
            ti値計算Class内部定義関数
            self._CalcTimeInterval(update_day) 
        Note:
        """    

        # TimeIntervalとHotSpot値を算出
        ti = self._CalcTimeInterval(updateDays)
        hs = 1.0 / (1 + np.exp(-12*ti+12))
        return ti, hs
