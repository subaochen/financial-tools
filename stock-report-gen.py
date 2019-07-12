# -*- coding: utf-8 -*-

import urllib3
import pandas as pd
import csv
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


def analyse_report(code, rows, cols):
    """
    分析报表
    Arguments:
        code:股票代码
        rows:读取报表的哪些行，接受列表
        cols:读取报表的哪些列，接受列表

    Return:
        获取的数据
    """
    filename = f'data/lrb_{code}.csv'
    df = pd.read_csv(filename)
    data = df.iloc[rows, cols]
    data.insert(0, '股票代码', code)
    return data

def each_record(codes, years, row='营业收入(万元)'):
    for code in codes:
        filename = f'data/lrb_{code}.csv'
        df = pd.read_csv(filename, index_col=0)
        x = df.loc[row, years]
        yield [code] + list(x)

if __name__ == '__main__':
    # 测试股票代码集合
    codes = ['603730', '603757']
    years = ['2018-12-31', '2017-12-31', '2016-12-31']
    #summary_data = []
    for code in codes:
        if DOWNLOAD == True:
            print(f"downloading report:{code}")
            download_report(code)
        # 第一列（2018年数据），第12行（研发费用）
        #data = analyse_report(code, [12], [1])
        #summary_data.append(data.values.tolist())

    summary = pd.DataFrame.from_records(each_record(codes, years), columns=['code'] + years)
    summary.to_csv('tmp.csv', index=False)

    #with open("summary.csv", "w+") as csvfile:
    #    writer = csv.writer(csvfile)
    #    # 根据情况写入表头
    #    writer.writerow(["股票代码", "研发费用(万元)"])
    #    # 写入多行用writerows
    #    for item in summary_data:
    #        writer.writerows(item)

