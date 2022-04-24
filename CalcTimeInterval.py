def CalcTimeInterval(update_day: datetime,hotspot_start_day:datetime) -> float:
    """HotSpot計算に必要となるit値を算出する

        修正が行われた時点のタイムスタンプでコードが生成されたときを0、現在を1と置いてその間の少数値をとります。
        つまり、12月1日にコードを書き始め、今日が12月30日であるとすると、15日にバグフィクスをしたらti=0.5になります。

    Args:
        update_day (datetime): モジュール修正日付 
        HopSpot測定開始基準日 (datetime):HotSpot測定開始日

    Returns:
        float: it算出結果

    Raises:
        例外の名前: 例外の説明 (例 : 引数が指定されていない場合に発生 )

    Examples:

        >>> calcTimeInterval (update_day, hotspot_start_day)

    Note:
        引数はdatetime型であり事前の変換が必要となる
        datetime.datetime及びdatetime.timedeltaのimport
            from datetime import datetime
            from datetime import timedalta

    """
    
    # 本日日付情報
    NOW = datetime.now()
    
    # ti値を算出
    return  float((update_day - hotspot_start_day + timedelta(days=1)).days) / \
            float((NOW - hotspot_start_day + timedelta(days=1)).days)
