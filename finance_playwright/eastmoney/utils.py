"""
各种HTTP和HTML的公共方法

翻页，第一页
"""


async def click_next_qtpager(page):
    await page.locator('div.qtpager a[title="下一页"]').click()


async def click_first_qtpager(page):
    if await page.locator('div.qtpager').count() > 0:
        await page.locator('div.qtpager').get_by_role("link", name="1", exact=True).click()


async def click_next_pagerbox(page):
    await page.locator('div.pagerbox a:text("下一页")').click()


async def click_first_pagerbox(page):
    if await page.locator('div.pagerbox').count() > 0:
        await page.locator('div.pagerbox a:not(:text("上一页"))').first.click()
