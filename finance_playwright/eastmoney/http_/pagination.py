from typing import Dict, List

import pandas as pd


def replace_hyphens(obj):
    """递归处理嵌套结构中的 '-'"""
    if isinstance(obj, dict):
        return {k: replace_hyphens(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_hyphens(item) for item in obj]
    elif obj == '-':
        return float('nan')
    return obj


class Pagination:
    def __init__(self):
        self.datas = {}
        self.page_no = 1
        self.page_size = 100
        self.total = 1024
        self.columns = []
        self.datas = {}

    def reset(self) -> None:
        self.datas = {}

    def update(self, page_no, page_size, total, columns, dataList) -> None:
        self.page_no = page_no
        self.page_size = page_size
        self.total = total
        self.columns = columns
        self.datas[self.page_no] = dataList

    def has_next(self, max_page) -> bool:
        c1 = self.page_no * self.page_size < self.total
        c2 = self.page_no < max_page
        return c1 & c2

    def current(self) -> int:
        return self.page_no

    def get_list(self) -> List:
        datas = []
        for k, v in self.datas.items():
            datas.extend(v)
        return datas

    def get_dataframe(self, column_name: Dict | None, column_func: Dict | None) -> pd.DataFrame:
        df = pd.DataFrame(replace_hyphens(self.get_list()))

        specified_order = self.columns
        # 获取指定顺序的列（只保留存在的列）
        ordered_cols = [col for col in specified_order if col in df.columns]
        # 获取未指定的列（保持原有顺序）
        remaining_cols = [col for col in df.columns if col not in specified_order]
        df = df.loc[:, ordered_cols + remaining_cols]

        if column_name:
            df = df.rename(columns=column_name)
        if column_func:
            for col_name, func in column_func.items():
                if col_name in df.columns:
                    df[col_name] = func(df[col_name])

        return df
