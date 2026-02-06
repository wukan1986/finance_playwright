import random

from finance_playwright.eastmoney.html_.api import bkzj, boards2, concept_board
from finance_playwright.playwright_helper import AsyncBrowser, get_edge_path


async def async_main():
    PROXYS = [
        None,
        {"server": "http://127.0.0.1:10808"},
        {"server": "http://localhost:10808"},
        # {"server": "http://[::1]:10808"},
    ]

    async with AsyncBrowser(endpoint="http://127.0.0.1:9222", executable_path=get_edge_path(), devtools=False, user_data_dir="D:\\user_data2") as browser:
        context = await browser.new_context(proxy=random.choice(PROXYS))
        page = await context.new_page()

        df = await boards2(page, "90", "BK0701", max_page=3)
        print(df)

        context = await browser.new_context(proxy=random.choice(PROXYS))
        page = await context.new_page()
        df = await bkzj(page, "BK0701", max_page=3)
        print(df)

        context = await browser.new_context(proxy=random.choice(PROXYS))
        page = await context.new_page()
        df = await concept_board(page, max_page=3)
        print(df)

        input("done")


if __name__ == "__main__":
    import asyncio

    asyncio.run(async_main())
