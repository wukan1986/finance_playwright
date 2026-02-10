import hashlib

from loguru import logger

from finance_playwright.eastmoney.utils import check_ad, check_valid, route_checkuser  # noqa
from finance_playwright.pagination import Pagination


async def goto_next(page, url1, func_read, func_goto, max_page: int = 2):
    # TODO 强行开启验证码弹出
    # await page.route("https://i.eastmoney.com/websitecaptcha/api/checkuser?callback=wsc_checkuser", route_checkuser)
    path = hashlib.md5(url1.encode("utf-8")).hexdigest() + '.pkl'

    p = Pagination(path)
    p.load()
    n = 1
    while n > 0:
        if n == 1:
            logger.info(url1)
            await page.goto(url1)  # 第二次到此不用担心，因为reload后goto不会刷新
            await check_ad(page)

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

    return p.get_dataframe(None, None, delete=True)
