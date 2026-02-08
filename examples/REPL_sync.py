"""
playwright codegen执行后，在Playwright Inspector工具的Locator面板可以实现定位高亮，但语法复杂点就无效
所以提供一个小工具，直接可输入代码执行，用于验证是否能快速定位
"""
from finance_playwright.playwright_helper import get_chrome_path, get_edge_path, kill_browsers, SyncBrowser  # noqa
from finance_playwright.utils import repl_sync


# 偶尔要关闭所有相关进程
# kill_browsers("msedge.exe")
# kill_browsers("chrome.exe")


def main():
    with SyncBrowser(endpoint="http://127.0.0.1:9222", executable_path=get_edge_path(), devtools=True) as browser:
        page = browser.get_page()
        # 定制你要访问的网站
        page.goto("https://quote.eastmoney.com/center/gridlist.html#boards2-90.BK0174")
        # 设置超时，加快验证过程
        page.set_default_timeout(2 * 1000)

        # page.get_by_role("link", name="下一页", exact=True).click()
        # page.get_by_role("link", name="下一页", exact=True).highlight()
        # page.get_by_role("link", name="下一页", exact=True).inner_html()
        repl_sync(globals(), locals())

        input("done")


if __name__ == "__main__":
    main()
