"""
通过HTTP协议解析获取数据

能读到更多界面不显示的数据
能读到更原始数子，非展示用的字符串
控制能力更强，可以一页更多数据

破解麻烦，工作量大

"""
from functools import lru_cache

import pandas as pd
import requests

from finance_playwright.eastmoney.http_ import column_name, column_func
from finance_playwright.eastmoney.http_.utils import goto_next
from finance_playwright.eastmoney.utils import click_next_qtpager, click_next_pagerbox


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


async def boards2(page, market: str = "90", code: str = "BK0732", max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 行业板块 > 贵金属"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#boards2-{market}.{code}"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=20&*"

    return await goto_next(page, URL1.format(market=market, code=code), URL2, URL3, column_name.bkchild, column_func.bkchild, click_next_qtpager, max_page=max_page)


async def concept_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 概念板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#concept_board"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=20&*"

    return await goto_next(page, URL1, URL2, URL3, column_name.bk_common, column_func.bk_common, click_next_qtpager, max_page=max_page)


async def region_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 地域板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#region_board"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=20&*"

    return await goto_next(page, URL1, URL2, URL3, column_name.bk_common, column_func.bk_common, click_next_qtpager, max_page=max_page)


async def industry_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 行业板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#industry_board"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=20&*"

    return await goto_next(page, URL1, URL2, URL3, column_name.bk_common, column_func.bk_common, click_next_qtpager, max_page=max_page)


async def bkzj(page, code: str = "BK0732", max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 数据中心 > 资金流向 > 概念资金流向 > 中证500"""
    URL1 = "https://data.eastmoney.com/bkzj/{code}.html"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=50&*"

    return await goto_next(page, URL1.format(code=code), URL2, URL3, column_name.BoardsCaptialFlow, column_func.BoardsCaptialFlow, click_next_pagerbox, max_page=max_page)


if __name__ == "__main__":
    df = get_bk_list()
    print(df)
