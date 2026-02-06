import json
from urllib.parse import urlparse, parse_qs

import pandas as pd
from loguru import logger

from finance_playwright.eastmoney.http_.pagination import Pagination
from finance_playwright.eastmoney.utils import click_dialog


async def modify_request(route, request):
    # 强行将每页20条改成每页100条。序号乱了，但内容正确
    url = request.url

    if "&pz=20&" in url:
        await route.continue_(url=url.replace("&pz=20&", "&pz=100&"))
    elif "&pz=50&" in url:
        await route.continue_(url=url.replace("&pz=50&", "&pz=100&"))
    else:
        await route.continue_()


async def goto_next(page, url1, url2, url3, new_columns, column_funcs, click_func, max_page: int = 100) -> pd.DataFrame:
    P = Pagination()

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
        print(total, pn, pz, len(diff), url)
        P.update(pn, pz, total, fields, diff)

    await page.route(url3, modify_request)

    P.reset()
    await page.goto(url1)
    # await click_dialog(page) # 好像不关，刷新一下就没了

    async with page.expect_response(url2) as response_info:
        await page.reload()
    await on_response(await response_info.value)

    while P.has_next(max_page):
        logger.info("当前页为:{}, 点击`下一页`", P.current())

        async with page.expect_response(url2) as response_info:
            await click_func(page)
        await on_response(await response_info.value)

    # import pickle
    # with open('1.pkl', 'wb') as f:
    #     pickle.dump(P.get_list(), f)

    return P.get_dataframe(new_columns, column_funcs)
