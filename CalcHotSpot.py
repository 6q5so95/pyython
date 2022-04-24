from datetime import datetime
from datetime import timedelta
import numpy as np
from typing import Tuple

class CalcHotSpot:
    """HotSpot計算に必要となるit値を算出する
        修正が行われた時点のタイムスタンプでコードが生成されたときを0、現在を1と置いてその間の少数値をとります。
        つまり、12月1日にコードを書き始め、今日が12月30日であるとすると、15日にバグフィクスをしたらti=0.5になります。
        
    """    
    
    def __init__(self, start_hotspot_day:datetime) -> None:
        self.start_hotspot_day = start_hotspot_day
        
    def CalcHotSpotValue(self, updateDays:datetime, date_now:datetime) -> Tuple[float, float]:
        """
        Args:
            update_day(datetime): HopSpot測定開始基準日
            date_now(datetime):   本日日付（テストのやりやすさからパラメータ化）
        Returns:
            float, float: ti値、hs値
        Raises:
            例外の名前: 例外の説明 (例 : 引数が指定されていない場合に発生 )
        Examples:
            >> hotspot = CalcHotSpot(HOTSPOT_STARTDATE)
            >> date_now = datetime.now()
            >> for _ in LIST_UPDATE_DATES:
            >>    ti, hs = hotspot.CalcHotSpotValue(_, date_now)
            >>    print(f'ti = {ti:9.05} hs = {hs:9.05f}')
        See:
        Note:
        """    

        # TODO 日付相関チェック
        # date_now >= update_day >= self.start_hotspot_day 

        # TimeIntervalとHotSpot値を算出
        ti = float((update_day - self.start_hotspot_day + timedelta(days=1)).days) / \
             float((date_now   - self.start_hotspot_day + timedelta(days=1)).days)        
        hs = 1.0 / (1 + np.exp(-12*ti+12))
        return ti, hs
