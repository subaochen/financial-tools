# -*- coding: utf-8 -*-

import urllib3
import pandas as pd
import os

# if DOWNLOAD = False，don't download report
DOWNLOAD=True

def download_report(code):
    """
    下载报表（利润表年表，如果下载其他报表，需要修改url

    Arguments:
        code: 股票代码
    """
    # 利润表(年表)
    url = f"http://quotes.money.163.com/service/lrb_{code}.html?type=year"
    base_dir='data'
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    report_file = f'{base_dir}/lrb_{code}.csv'
    http = urllib3.PoolManager()

    response = http.request('GET', url)
    with open(report_file, 'wb') as f:
        # 163网页的编码是gbk，需要转成utf-8
        f.write(response.data.decode('gbk').encode('utf-8'))


# 默认获取研发费用，修改row可以获取其他资料
def each_record(codes, years, row='研发费用(万元)'):
    for code in codes:
        filename = f'data/lrb_{code}.csv'
        df = pd.read_csv(filename, index_col=0)
        x = df.loc[row, years]
        yield [code] + list(x)

if __name__ == '__main__':
    # 测试股票代码集合
    codes = ['603730', '603757']
    years = ['2018-12-31', '2017-12-31']
    for code in codes:
        if DOWNLOAD == True:
            print(f"downloading report:{code}")
            download_report(code)

    summary = pd.DataFrame.from_records(each_record(codes, years), columns=['code'] + years)
    summary.to_csv('summary.csv', index=False)

