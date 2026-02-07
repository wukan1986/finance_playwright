from io import StringIO

import pandas as pd
from loguru import logger

from finance_playwright.eastmoney.utils import click_next_qtpager, click_next_pagerbox


async def read_quotetable(page, url1, max_page: int = 2):
    # https://quote.eastmoney.com/center/gridlist.html#boards2-90.BK0149
    # https://quote.eastmoney.com/center/gridlist.html#nobalmetal_futures
    async def _table(page):
        table_html = await page.locator('div[class=quotetable] table').evaluate("element => element.outerHTML")
        df = pd.read_html(StringIO(table_html))[0]

        if await page.locator('div.qtpager').count() > 0:
            current_page = int(await page.locator('div.qtpager a.acitve').text_content())  # active
            last_page = int(await page.locator('div.qtpager a:not([title="下一页"])').last.text_content())
        else:
            current_page = 1
            last_page = 1

        return df, current_page, last_page

    await page.goto(url1)
    # await click_dialog(page) # 好像不关，刷新一下就没了
    await page.reload()

    dfs = []
    for i in range(max_page):
        df, current_page, last_page = await _table(page)
        dfs.append(df)
        if current_page < min(last_page, max_page):
            logger.info("当前页为:{}, 点击`下一页`", current_page)
            await click_next_qtpager(page)
        else:
            break

    return pd.concat(dfs)


async def read_dataview(page, url1, max_page: int = 2):
    # https://data.eastmoney.com/bkzj/BK0731.html
    # https://data.eastmoney.com/bkzj/BK0701.html
    async def _table(page):
        table_html = await page.locator('div[class=dataview-body] table').evaluate("element => element.outerHTML")
        df = pd.read_html(StringIO(table_html))[0]

        if await page.locator('div.pagerbox').count() > 0:
            current_page = int(await page.locator('div.pagerbox a.active').text_content())
            last_page = int(await page.locator('div.pagerbox a:not(:text-is("下一页"))').last.text_content())
        else:
            current_page = 1
            last_page = 1

        return df, current_page, last_page

    await page.goto(url1)
    # await click_dialog(page) # 好像不关，刷新一下就没了
    await page.reload()

    dfs = []
    for i in range(max_page):
        df, current_page, last_page = await _table(page)
        dfs.append(df)
        if current_page < min(last_page, max_page):
            logger.info("当前页为:{}, 点击`下一页`", current_page)
            await click_next_pagerbox(page)
        else:
            break

    return pd.concat(dfs)
