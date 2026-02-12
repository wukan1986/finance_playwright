from fake_useragent import UserAgent

from finance_playwright.eastmoney.http_.api import bkzj, boards2, concept_board, cjsj_cpi, cjsj_foreign_0_2, cjsj_foreign_0_4
from finance_playwright.playwright_helper import AsyncBrowser, get_chrome_path, get_edge_path, kill_browsers  # noqa
from finance_playwright.utils import browser_retry

# kill_browsers("msedge.exe")
# kill_browsers("chrome.exe")

PROXYS = [
    None,
    # {"server": "http://127.0.0.1:10808"},
    # {"server": "http://localhost:10808"},
    # {"server": "http://[::1]:10808"},
]
ua = UserAgent(browsers=['Edge', 'Chrome'])


async def main():
    async with AsyncBrowser(endpoint="http://127.0.0.1:9222", executable_path=get_edge_path(), devtools=True, user_data_dir="D:\\user_data2") as browser:
        await browser_retry(browser, PROXYS, ua, boards2, "90", "BK0701", max_page=3)
        await browser_retry(browser, PROXYS, ua, bkzj, "BK0701", max_page=3)
        await browser_retry(browser, PROXYS, ua, concept_board, max_page=3)
        await browser_retry(browser, PROXYS, ua, cjsj_cpi)
        await browser_retry(browser, PROXYS, ua, cjsj_foreign_0_2)
        await browser_retry(browser, PROXYS, ua, cjsj_foreign_0_4)

        input("done")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
