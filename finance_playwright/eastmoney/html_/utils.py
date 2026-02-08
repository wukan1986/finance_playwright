import random

from loguru import logger

from finance_playwright.eastmoney.html_.pagination import Pagination
from finance_playwright.utils import repl_async  # noqa


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


async def check_ad(page):
    if (await page.locator('img.wztctg').count()) > 0:
        logger.info("发现弹出广告")
        await page.locator('img[onclick="tk_tg_zoomin()"]').click()
        await page.wait_for_selector("img.wztctg", state="detached", timeout=0)
        return True
    else:
        return False


async def goto_next(page, url1, func_read, func_goto, max_page: int = 2):
    # TODO 强行开启验证码弹出
    # await page.route("https://i.eastmoney.com/websitecaptcha/api/checkuser?callback=wsc_checkuser", route_checkuser)

    logger.info(url1)
    await page.goto(url1)
    await check_ad(page)

    p = Pagination()
    n = 1
    while n > 0:
        df, current_page, last_page = await func_read(page)
        p.update2(current_page, last_page)
        if await check_valid(page):
            n = p.next(max_page)
            logger.info("有验证，跳过当前页:{}, 翻页到:{}", p.current(), n)
        else:
            if not df.empty:
                logger.info("更新数据,{}", current_page)
                p.update3(current_page, last_page, df)
            n = p.next(max_page)
            logger.info("无验证，有效当前页:{}, 翻页到:{}", p.current(), n)

        if n == 1 or n == p.current():
            await page.reload()
            continue

        if n > 1:
            await func_goto(page, n)
            continue

    return p.get_dataframe()
