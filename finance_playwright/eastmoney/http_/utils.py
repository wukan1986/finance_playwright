import hashlib
import json
from urllib.parse import urlparse, parse_qs

import pandas as pd
from loguru import logger
from playwright.sync_api import TimeoutError

from finance_playwright.eastmoney.utils import check_ad, check_valid, check_loading
from finance_playwright.pagination import Pagination


async def modify_request(route, request):
    # 强行将每页20条改成每页100条。序号乱了，但内容正确
    url = request.url

    if "&pz=20&" in url:
        await route.continue_(url=url.replace("&pz=20&", "&pz=100&"))
    elif "&pz=50&" in url:
        await route.continue_(url=url.replace("&pz=50&", "&pz=100&"))
    else:
        await route.continue_()


async def goto_next(page, url1: str, url2: str, url3: str, new_columns, column_funcs, goto_func, max_page: int = 100) -> pd.DataFrame:
    # TODO 强行开启验证码弹出
    # await page.route("https://i.eastmoney.com/websitecaptcha/api/checkuser?callback=wsc_checkuser", route_checkuser)
    path = hashlib.md5(url1.encode("utf-8")).hexdigest() + '.pkl'

    p = Pagination(path)
    p.load()

    async def on_response(response):
        url = response.url
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        pn = int(query_params['pn'][0])
        pz = int(query_params['pz'][0])
        fields = query_params['fields'][0].split(',')

        text = await response.text()
        json_str = text[text.find('(') + 1:text.rfind(')')]
        data = json.loads(json_str)
        total = data['data']['total']
        diff = data['data']['diff']
        logger.info("更新数据，当前页:{}, 每页大小:{}，总数:{}, {}", pn, pz, total, url)
        p.update5(pn, pz, total, fields, diff)

    if url2 != url3:
        await page.route(url3, modify_request)

    n = 1
    while n > 0:
        try:
            async with page.expect_response(url2, timeout=10000) as response_info:
                p.update1(n)
                if n == 1:
                    logger.info(url1)
                    await page.goto(url1)
                else:
                    if p.current() == n:
                        logger.info("当前页:{}, 翻页到:{}", p.current(), n)
                        await page.reload()
                    else:
                        # 有可能刷要翻页时一直loading
                        logger.info("当前页:{}, 翻页到:{}", p.current(), n)
                        # await repl_async(globals(), locals(), quit_on_enter=True)
                        await goto_func(page, n)
            await on_response(await response_info.value)
        except TimeoutError as e:
            print(f"超时错误: {e}")
            if await check_loading(page):
                logger.info("发现数据加载时间过长，新建context")
                p.save()
                raise
        if n == 1:
            await check_ad(page)
        await check_valid(page)
        n = p.next(max_page)

    return p.get_dataframe(new_columns, column_funcs, delete=True)


async def goto_one(page, url1: str, url2: str) -> pd.DataFrame:
    path = hashlib.md5(url1.encode("utf-8")).hexdigest() + '.pkl'

    p = Pagination(path)
    p.load()

    async def on_response(response):
        url = response.url

        text = await response.text()
        json_str = text[text.find('(') + 1:text.rfind(')')]
        d = json.loads(json_str)
        count = d['result']['count']
        pages = d['result']['pages']
        data = d['result']['data']
        logger.info("更新数据，总数:{}, {}", count, url)
        p.update5(1, 10000, count, [], data)

    async with page.expect_response(url2, timeout=10000) as response_info:
        logger.info(url1)
        await page.goto(url1)
    await on_response(await response_info.value)
    await check_ad(page)

    return p.get_dataframe(None, None, delete=True)
