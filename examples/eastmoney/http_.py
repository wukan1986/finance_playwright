import logging
import random

from fake_useragent import UserAgent
from loguru import logger
from playwright_stealth import Stealth
from tenacity import retry, stop_after_attempt, wait_random, before_sleep_log

from finance_playwright.eastmoney.http_.api import bkzj, boards2, concept_board
from finance_playwright.playwright_helper import AsyncBrowser, get_chrome_path, get_edge_path, kill_browsers  # noqa

# kill_browsers("msedge.exe")
# kill_browsers("chrome.exe")

PROXYS = [
    None,
    # {"server": "http://127.0.0.1:10808"},
    # {"server": "http://localhost:10808"},
    # {"server": "http://[::1]:10808"},
]
ua = UserAgent(browsers=['Edge', 'Chrome'])


@retry(stop=stop_after_attempt(3), wait=wait_random(10, 20), before_sleep=before_sleep_log(logger, logging.DEBUG))
async def browser_retry(browser, func, *arg, **kwargs):
    proxy = random.choice(PROXYS)
    user_agent = ua.random
    print(proxy, user_agent)
    context = await browser.new_context(proxy=proxy, user_agent=user_agent)
    await Stealth().apply_stealth_async(context)
    page = await context.new_page()
    df = await func(page, *arg, **kwargs)
    # TODO 这里可以保存一下
    print(df)


async def main():
    async with AsyncBrowser(endpoint="http://127.0.0.1:9222", executable_path=get_edge_path(), devtools=True, user_data_dir="D:\\user_data2") as browser:
        await browser_retry(browser, boards2, "90", "BK0701", max_page=3)
        await browser_retry(browser, bkzj, "BK0701", max_page=3)
        await browser_retry(browser, concept_board, max_page=3)

        input("done")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
