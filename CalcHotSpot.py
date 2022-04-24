from datetime import datetime
from datetime import timedelta
import numpy as np
from typing import Tuple

class CalcHotSpot:
    def __init__(self, start_hotspot_day):
        self.start_hotspot_day = start_hotspot_day
    
    def _CalcTimeInterval(self, update_day: datetime) -> float:
        # 本日日付情報
        NOW = datetime.now()
    
        # ti値を算出
        return  float((update_day - self.start_hotspot_day + timedelta(days=1)).days) / \
                float((NOW - self.start_hotspot_day + timedelta(days=1)).days)
    
    def CalcHotSpotValue(self, updateDays:datetime) -> Tuple[float, float]:
        # TimeIntervalとHotSpot値を算出
        ti = self._CalcTimeInterval(updateDays)
        hs = 1.0 / (1 + np.exp(-12*ti+12))
        return ti, hs
