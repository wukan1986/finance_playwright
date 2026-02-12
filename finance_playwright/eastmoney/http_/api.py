"""
通过HTTP协议解析获取数据

能读到更多界面不显示的数据
能读到更原始数子，非展示用的字符串
控制能力更强，可以一页更多数据

破解麻烦，工作量大

"""

import pandas as pd

from finance_playwright.eastmoney.http_ import column_name, column_func
from finance_playwright.eastmoney.http_.utils import goto_next, goto_one
from finance_playwright.eastmoney.utils import click_goto_qtpager, click_goto_pagerbox


async def boards2(page, market: str = "90", code: str = "BK0732", max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 行业板块 > 贵金属"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#boards2-{market}.{code}"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=20&*"

    return await goto_next(page, URL1.format(market=market, code=code), URL2, URL3, column_name.bkchild, column_func.bkchild, click_goto_qtpager, max_page=max_page)


async def concept_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 概念板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#concept_board"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=20&*"

    return await goto_next(page, URL1, URL2, URL3, column_name.bk_common, column_func.bk_common, click_goto_qtpager, max_page=max_page)


async def region_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 地域板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#region_board"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=20&*"

    return await goto_next(page, URL1, URL2, URL3, column_name.bk_common, column_func.bk_common, click_goto_qtpager, max_page=max_page)


async def industry_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 行业板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#industry_board"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=20&*"

    return await goto_next(page, URL1, URL2, URL3, column_name.bk_common, column_func.bk_common, click_goto_qtpager, max_page=max_page)


async def bkzj(page, code: str = "BK0732", max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 数据中心 > 资金流向 > 概念资金流向 > 中证500"""
    URL1 = "https://data.eastmoney.com/bkzj/{code}.html"
    URL2 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=100&*"
    URL3 = "https://push2.eastmoney.com/api/qt/clist/get?*&pz=50&*"

    return await goto_next(page, URL1.format(code=code), URL2, URL3, column_name.BoardsCaptialFlow, column_func.BoardsCaptialFlow, click_goto_pagerbox, max_page=max_page)


async def cjsj_cpi(page):
    """中国 居民消费价格指数(CPI，上年同月=100)

    财经数据_CPI
    """
    URL1 = "https://data.eastmoney.com/cjsj/cpi.html"
    URL2 = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery*&reportName=RPT_ECONOMY_CPI&*"
    return await goto_one(page, URL1, URL2)


async def cjsj_ppi(page):
    """中国 工业品出厂价格指数(PPI)"""
    URL1 = "https://data.eastmoney.com/cjsj/ppi.html"
    URL2 = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery*"
    return await goto_one(page, URL1, URL2)


async def cjsj_gdp(page):
    """中国 国内生产总值(GDP)"""
    URL1 = "https://data.eastmoney.com/cjsj/gdp.html"
    URL2 = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery*"
    return await goto_one(page, URL1, URL2)


async def cjsj_foreign_0_2(page):
    """美国 非农就业人数变化

    Notes
    -----
    数据发布时间有误

    例如：2026年2月11日发布的数据，但显示的2026年2月6日。但从Choice终端上查询又是正确的

    """
    URL1 = "https://data.eastmoney.com/cjsj/foreign_0_2.html"
    URL2 = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery*"
    return await goto_one(page, URL1, URL2)


async def cjsj_foreign_0_4(page):
    """美国 失业率

    Notes
    -----
    数据发布时间有误

    例如：2026年2月11日发布的数据，但显示的2026年2月6日。但从Choice终端上查询又是正确的

    """
    URL1 = "https://data.eastmoney.com/cjsj/foreign_0_4.html"
    URL2 = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery*"
    return await goto_one(page, URL1, URL2)
