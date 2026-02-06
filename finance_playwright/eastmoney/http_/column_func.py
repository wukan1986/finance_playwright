bk_common = {
    '最新价': lambda x: x / 1e2,
    '涨跌额': lambda x: x / 1e2,
    '涨跌幅': lambda x: x / 1e4,
    '总市值': lambda x: x / 1e8,
    '换手率': lambda x: x / 1e4,
    '领涨股票涨跌幅': lambda x: x / 1e4,
    '领跌股票涨跌幅': lambda x: x / 1e4,
}

bkchild = {
    '最新价': lambda x: x / 1e2,
    '涨跌额': lambda x: x / 1e2,
    '涨跌幅': lambda x: x / 1e4,
    '成交量(手)': lambda x: x / 1e4,
    '成交额': lambda x: x / 1e8,
    '振幅': lambda x: x / 1e4,
    '最高': lambda x: x / 1e2,
    '昨收': lambda x: x / 1e2,
    '最低': lambda x: x / 1e2,
    '今开': lambda x: x / 1e2,
    '量比': lambda x: x / 1e2,
    '换手率': lambda x: x / 1e4,
    '市盈率(动态)': lambda x: x / 1e2,
    '市净率': lambda x: x / 1e2,
}

BoardsCaptialFlow = {
    '今日涨跌幅': lambda x: x / 1e2,
    '今日主力净流入净额': lambda x: x / 1e8,
    '今日主力净流入净占比': lambda x: x / 1e2,
    '今日超大单净流入净额': lambda x: x / 1e8,
    '今日超大单净流入净占比': lambda x: x / 1e2,
    '今日大单净流入净额': lambda x: x / 1e8,
    '今日大单净流入净占比': lambda x: x / 1e2,
    '今日中单净流入净额': lambda x: x / 1e8,
    '今日中单净流入净占比': lambda x: x / 1e2,
    '今日小单净流入净额': lambda x: x / 1e8,
    '今日小单净流入净占比': lambda x: x / 1e2,
}
