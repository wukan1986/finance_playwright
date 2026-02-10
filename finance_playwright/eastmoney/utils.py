"""
各种HTTP和HTML的公共方法

翻页，第一页
"""
import random
from io import StringIO

import pandas as pd
from loguru import logger

from finance_playwright.utils import repl_async  # noqa


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


# =======================================
async def route_checkuser(route):
    # 获取原始响应
    response = await route.fetch()
    text = await response.text()

    # 返回修改后的响应
    if random.random() > 0:
        text = text.replace('false', 'true')

    await route.fulfill(body=text)


async def check_valid(page):
    """检查特定响应后是否出现弹窗"""
    if (await page.locator("div.popwscps_d").count()) > 0:
        logger.info("发现滑动验证码")

        import winsound
        duration = 1500  # 持续时间，单位为毫秒
        frequency = 700  # 频率，单位为赫兹
        winsound.Beep(frequency, duration)
        # TODO 编辑此处，进行自动操作
        await page.frame_locator('iframe.popwscps_d_iframe').locator('a.em_refresh_button').highlight()
        # TODO 开启交互功能
        # await repl_async(globals(), locals(), quit_on_enter=True)
        await page.wait_for_selector("div.popwscps_d", state="detached", timeout=0)
        return True
    else:
        return False


async def check_loading(page) -> bool:
    return await page.locator("div[class=dataview-loading]").is_visible()


async def check_ad(page):
    if (await page.locator('img.wztctg').count()) > 0:
        logger.info("发现弹出广告")
        await page.locator('img[onclick="tk_tg_zoomin()"]').click()
        await page.wait_for_selector("img.wztctg", state="detached", timeout=0)
        return True
    else:
        return False
