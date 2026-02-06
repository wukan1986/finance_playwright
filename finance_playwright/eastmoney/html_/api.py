"""
解析HTML页面元素

通用性最强，不需代码破解
但格式丢失，因为数字带了单位，导致保持成字符串格式
部分数据丢失，因为传递了根多数据，但部分不显示导致提取不到

只能读取表，不能读图

"""
import pandas as pd

from finance_playwright.eastmoney.html_.utils import read_quotetable, read_dataview


async def boards2(page, market: str = "90", code: str = "BK0732", max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 行业板块 > 贵金属"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#boards2-{market}.{code}"
    return await read_quotetable(page, URL1.format(market=market, code=code), max_page=max_page)


async def concept_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 概念板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#concept_board"
    return await read_quotetable(page, URL1, max_page=max_page)


async def region_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 地域板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#region_board"
    return await read_quotetable(page, URL1, max_page=max_page)


async def industry_board(page, max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 行情中心 > 沪深京板块 > 行业板块"""
    URL1 = "https://quote.eastmoney.com/center/gridlist.html#industry_board"
    return await read_quotetable(page, URL1, max_page=max_page)


async def bkzj(page, code: str = "BK0732", max_page: int = 2) -> pd.DataFrame:
    """东方财富网 > 数据中心 > 资金流向 > 概念资金流向 > 中证500"""
    URL1 = "https://data.eastmoney.com/bkzj/{code}.html"
    return await read_dataview(page, URL1.format(code=code), max_page=max_page)
