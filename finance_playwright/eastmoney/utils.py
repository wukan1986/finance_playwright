"""
各种HTTP和HTML的公共方法

翻页，第一页
"""
import re


async def click_next_qtpager(page):
    if await page.locator('div.qtpager').count() > 0:
        await page.locator('div.qtpager').get_by_title("下一页", exact=True).click()


async def click_first_qtpager(page):
    if await page.locator('div.qtpager').count() > 0:
        await page.locator('div.qtpager').get_by_role("link", name="1", exact=True).click()


async def click_next_pagerbox(page):
    if await page.locator('div.pagerbox').count() > 0:
        await page.locator("div.pagerbox").get_by_text("下一页", exact=True).click()


async def click_first_pagerbox(page):
    if await page.locator('div.pagerbox').count() > 0:
        await page.locator("div.pagerbox").get_by_role("link", name="1", exact=True).click()


async def click_dialog(page):
    try:
        close_selector = 'img[onclick*="tk_tg_zoomin"]'
        close_button = await page.wait_for_selector(close_selector, timeout=5000)
        await close_button.click()
        print("检测到弹窗并已关闭。")
    except:
        print("弹窗未出现，正常继续。")
