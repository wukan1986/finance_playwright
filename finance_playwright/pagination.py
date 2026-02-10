import itertools
import math
import pathlib
import pickle
from typing import Dict, List

import pandas as pd


def replace_hyphens(obj):
    """递归处理嵌套结构中的 '-'"""
    if isinstance(obj, dict):
        return {k: replace_hyphens(v) for k, v in obj.items()}
    elif isinstance(obj, (list, itertools.chain)):
        return [replace_hyphens(item) for item in obj]
    elif obj == '-':
        return float('nan')
    return obj


class Pagination:
    def __init__(self, path: str) -> None:
        self.path = pathlib.Path(path)
        self.datas = {}
        self.page_no = 1
        self.page_last = 100
        self.page_size = 50
        self.total = 1024
        self.columns = []
        self.datas = {}
        self.idx = 0

    def update1(self, idx: int) -> None:
        self.idx = idx

    def update2(self, page_no, page_last):
        self.page_no = page_no
        self.page_last = page_last
        self.idx = page_no

    def update3(self, page_no, page_last, df):
        self.page_no = page_no
        self.page_last = page_last
        self.idx = page_no
        self.datas[self.page_no] = df

    def update5(self, page_no: int, page_size: int, total: int, columns, data) -> None:
        # 数据中有当前页码，每页大小，总数
        self.page_no = page_no
        self.page_size = page_size
        self.page_last = math.ceil(self.total / self.page_size)
        self.idx = page_no
        self.total = total
        self.columns = columns
        self.datas[self.page_no] = data

    def next(self, max_page: int) -> int:
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

    def get_dataframe(self, column_name: Dict | None, column_func: Dict | None, delete: bool = False) -> pd.DataFrame:
        datas = self.get_list()
        if isinstance(datas[0], pd.DataFrame):
            df = pd.concat(self.get_list())
        else:
            datas = replace_hyphens(itertools.chain.from_iterable(datas))
            df = pd.DataFrame(datas)

        if self.columns:
            specified_order = self.columns
            ordered_cols = [col for col in specified_order if col in df.columns]
            remaining_cols = [col for col in df.columns if col not in specified_order]
            df = df.loc[:, ordered_cols + remaining_cols]

        if column_name:
            df = df.rename(columns=column_name)
        if column_func:
            for col_name, func in column_func.items():
                if col_name in df.columns:
                    df[col_name] = func(df[col_name])

        if delete:
            self.path.unlink(missing_ok=True)

        return df

    def save(self) -> None:
        with self.path.open("wb") as f:
            pickle.dump(self.datas, f)

    def load(self) -> None:
        if self.path.exists():
            with self.path.open("rb") as f:
                self.datas = pickle.load(f)


if __name__ == "__main__":
    import random

    a = random.sample(range(1, 6), 5)
    p = Pagination()
    for i in range(5):
        print(p.datas.keys())
        print(p.next(5))
        p.update5(a[i], 5, 100, [], pd.DataFrame([a[i]]))
        print(p.datas.keys())

    print(p.get_list())
    print(p.datas.keys())
