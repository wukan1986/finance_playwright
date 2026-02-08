"""
希望能随机的下载页面，然后顺序拼出

保证能中断后还能恢复下载
"""
import random
from typing import List

import pandas as pd


class Pagination:
    def __init__(self):
        self.datas = {}
        self.page_no = 1
        self.page_last = 100
        self.columns = []
        self.datas = {}
        self.idx = 0

    def reset(self) -> None:
        self.datas = {}

    def update2(self, page_no, page_last):
        self.page_no = page_no
        self.page_last = page_last
        self.idx = page_no

    def update3(self, page_no, page_last, df):
        self.page_no = page_no
        self.page_last = page_last
        self.idx = page_no
        self.datas[self.page_no] = df

    def next(self, max_page) -> int:
        # 默认第一页都要记录，所以长度就是页数
        max_page = min(max_page, self.page_last)
        if len(self.datas) >= max_page:
            return -1

        for i in range(max_page):
            self.idx %= max_page
            self.idx += 1
            if self.idx not in self.datas:
                return self.idx

        return -1

    def current(self) -> int:
        return self.page_no

    def get_list(self) -> List:
        self.datas = dict(sorted(self.datas.items()))
        datas = []
        for k, v in self.datas.items():
            datas.append(v)
        return datas

    def get_dataframe(self) -> pd.DataFrame:
        return pd.concat(self.get_list())


if __name__ == "__main__":
    a = random.sample(range(1, 6), 5)
    p = Pagination()
    for i in range(5):
        print(p.datas.keys())
        print(p.next(5))
        p.update3(a[i], 5, pd.DataFrame([a[i]]))
        print(p.datas.keys())

    print(p.get_list())
    print(p.datas.keys())
