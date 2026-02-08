"""
各种HTTP和HTML的公共方法

翻页，第一页
"""
from io import StringIO

import pandas as pd


async def click_next_qtpager(page):
    if await page.locator("div.qtpager").count() > 0:
        await page.locator("div.qtpager").get_by_title("下一页", exact=True).click()


async def click_first_qtpager(page):
    if await page.locator("div.qtpager").count() > 0:
        await page.locator("div.qtpager").get_by_role("link", name="1", exact=True).click()


async def click_goto_qtpager(page, n: int):
    form = page.locator("form.gotoform")
    if await form.count() > 0:
        await form.get_by_role("textbox").fill(str(n))
        await form.get_by_role("button", name="GO").click()


async def read_quotetable_1(page):
    table_html = await page.locator('div.quotetable table').evaluate("element => element.outerHTML")
    df = pd.read_html(StringIO(table_html), converters={"代码": str})[0]

    if await page.locator('div.qtpager').count() > 0:
        current_page = int(await page.locator('div.qtpager a.acitve').text_content())  # active
        last_page = int(await page.locator('div.qtpager a:not([title="下一页"])').last.text_content())
    else:
        current_page = 1
        last_page = 1

    return df, current_page, last_page


# =======================================

async def click_next_pagerbox(page):
    if await page.locator("div.pagerbox").count() > 0:
        await page.locator("div.pagerbox").get_by_text("下一页", exact=True).click()


async def click_first_pagerbox(page):
    if await page.locator("div.pagerbox").count() > 0:
        await page.locator("div.pagerbox").get_by_role("link", name="1", exact=True).click()


async def click_goto_pagerbox(page, n: int):
    form = page.locator("div.gotopage")
    if await form.count() > 0:
        await form.get_by_role("textbox").fill(str(n))
        await form.get_by_role("button", name="确定").click()


async def read_dataview_1(page):
    table_html = await page.locator('div[class=dataview-body] table').evaluate("element => element.outerHTML")
    df = pd.read_html(StringIO(table_html), converters={"代码": str})[0]

    if await page.locator('div.pagerbox').count() > 0:
        current_page = int(await page.locator('div.pagerbox a.active').text_content())
        last_page = int(await page.locator('div.pagerbox a:not(:text-is("下一页"))').last.text_content())
    else:
        current_page = 1
        last_page = 1

    return df, current_page, last_page
