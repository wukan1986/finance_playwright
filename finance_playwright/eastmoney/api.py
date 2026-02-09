from functools import lru_cache

import pandas as pd
import requests


@lru_cache
def get_bk_list() -> pd.DataFrame:
    """获取板块名和代码的对应清单

    访问地址：https://quote.eastmoney.com/center/hsbk.html

    Returns
    -------
    pd.DataFrame

    """
    URL = "https://quote.eastmoney.com/center/api/sidemenu_new.json"
    response = requests.get(URL)
    json_obj = response.json()
    df = pd.DataFrame.from_records(json_obj['bklist'])
    return df


if __name__ == "__main__":
    df = get_bk_list()
    print(df)