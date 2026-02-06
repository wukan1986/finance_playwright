# finance_playwright

自动化财务数据提取练手项目。使用`playwright`控制浏览器下载数据，虽然比`requests`慢，但通用性更好

## 安装部署

```commandline
git clone --depth=1 https://github.com/wukan1986/finance_playwright.git
cd finance_playwright
uv venv
uv build
```

## 爬取方式一HTTP

通过解析`HTTP`请求返回的`json`数据，得到目标数据

1. 获取的底层更原始数据，含有更多信息，保持了原始数据类型
2. 开发工作量大，不同页面要分别处理

## 爬取方式二HTML

通过解析`HTML`网页`DOM`，得到目标数据

1. 仅获取展示的界面，数字先变成了字符串，可能转不回数字
2. 开发简单,通用性更高

## 代理池

可以为不同请求启用新的`context`，实现分别设置代理

```python
context = await browser.new_context(proxy={"server": "http://127.0.0.1:10808"})
page = await context.new_page()
```