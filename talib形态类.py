import pymysql
import talib
import pandas as pd


def get_data(code='300003', start_date='2014-01-01', end_date='2023-04-01'):
    conn = pymysql.connect(host='localhost', user='root', password='Pass2006', database='stock')
    cursor = conn.cursor()
    sql = "SELECT date,open_price,high_price,low_price,close_price,volume," \
          "turn_volume as Tv,change_radio as Cr,increase_decrease as Inc,increase_decrease_radio as Incr" \
          " FROM daily " "WHERE code = %s AND date BETWEEN %s AND %s order by date "
    cursor.execute(sql, (code, start_date, end_date))

    # 读取查询结果
    results = cursor.fetchall()
    data = pd.DataFrame(results, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'Tv', 'Cr', 'Inc', 'Incr'])
    data['date'] = pd.to_datetime(data['date'])
    # data['Open'] = pd.to_numeric(data['Open'])
    # data['High'] = pd.to_numeric(data['High'])
    # data['Low'] = pd.to_numeric(data['Low'])
    # data['Close'] = pd.to_numeric(data['Close'])
    # data['Tv'] = pd.to_numeric(data['Tv'])
    # data['Cr'] = pd.to_numeric(data['Cr'])
    # data['Inc'] = pd.to_numeric(data['Inc'])
    # data['Incr'] = pd.to_numeric(data['Incr'])
    data.set_index('date', inplace=True)
    data.index = pd.to_datetime(data.index)
    return data


class TalibCdls():

    def __init__(self, data):
        self.data = data
        self.cdlf = [['CDL2CROWS', '2只乌鸦'], ['CDL3BLACKCROWS', '3只黑乌鸦'], ['CDL3INSIDE', '三内部上涨和下跌'],
                     ['CDL3LINESTRIKE', '三线打击'], ['CDL3OUTSIDE', '三外部上涨和下跌'],
                     ['CDL3STARSINSOUTH', '南方三星'],
                     ['CDL3WHITESOLDIERS', '三个白兵'], ['CDLABANDONEDBABY', '弃婴'], ['CDLADVANCEBLOCK', '大敌当前'],
                     ['CDLBELTHOLD', '捉腰带线'], ['CDLBREAKAWAY', '脱离'], ['CDLCLOSINGMARUBOZU', '收盘缺影线'],
                     ['CDLCONCEALBABYSWALL', '藏婴吞没'], ['CDLCOUNTERATTACK', '反击线'],
                     ['CDLDARKCLOUDCOVER', '乌云压顶'],
                     ['CDLDOJI', '十字'], ['CDLDOJISTAR', '十字星'], ['CDLDRAGONFLYDOJI', '蜻蜓十字T形十字'],
                     ['CDLENGULFING', '吞噬模式'], ['CDLEVENINGDOJISTAR', '十字暮星'], ['CDLEVENINGSTAR', '暮星'],
                     ['CDLGAPSIDESIDEWHITE', '向上或下跳空并列阳线'], ['CDLGRAVESTONEDOJI', '墓碑十字倒T十字'],
                     ['CDLHAMMER', '锤头'],
                     ['CDLHANGINGMAN', '上吊线'], ['CDLHARAMI', '母子线'], ['CDLHARAMICROSS', '十字孕线'],
                     ['CDLHIGHWAVE', '风高浪大线'], ['CDLHIKKAKE', '陷阱'], ['CDLHIKKAKEMOD', '修正陷阱'],
                     ['CDLHOMINGPIGEON', '家鸽'], ['CDLIDENTICAL3CROWS', '三胞胎乌鸦'], ['CDLINNECK', '颈内线'],
                     ['CDLINVERTEDHAMMER', '倒锤头'], ['CDLKICKING', '反冲形态'],
                     ['CDLKICKINGBYLENGTH', '由较长缺影线决定的反冲形态'],
                     ['CDLLADDERBOTTOM', '梯底'], ['CDLLONGLEGGEDDOJI', '长脚十字'], ['CDLLONGLINE', '长蜡烛'],
                     ['CDLMARUBOZU', '光头光脚/缺影线'], ['CDLMATCHINGLOW', '相同低价'], ['CDLMATHOLD', '铺垫'],
                     ['CDLMORNINGDOJISTAR', '十字晨星'], ['CDLMORNINGSTAR', '晨星'], ['CDLONNECK', '颈上线'],
                     ['CDLPIERCING', '刺透形态'], ['CDLRICKSHAWMAN', '黄包车夫'],
                     ['CDLRISEFALL3METHODS', '上升/下降三法'],
                     ['CDLSEPARATINGLINES', '分离线'], ['CDLSHOOTINGSTAR', '射击之星'], ['CDLSHORTLINE', '短蜡烛'],
                     ['CDLSPINNINGTOP', '纺锤'], ['CDLSTALLEDPATTERN', '停顿形态'], ['CDLSTICKSANDWICH', '条形三明治'],
                     ['CDLTAKURI', '探水竿'], ['CDLTASUKIGAP', '跳空并列阴阳线'], ['CDLTHRUSTING', '插入'],
                     ['CDLTRISTAR', '三星'], ['CDLUNIQUE3RIVER', '奇特三河床'],
                     ['CDLUPSIDEGAP2CROWS', '向上跳空的两只乌鸦'],
                     ['CDLXSIDEGAP3METHODS', '上升/下降跳空三法']]

    def cdls(self, indicator_name):
        func = getattr(talib, indicator_name)
        return func(self.data['open'], self.data['high'], self.data['low'], self.data['close'])


stock_code = '600000'
datas = get_data()
ti = TalibCdls(datas)

for dd in ti.cdlf:
    res_cdls = ti.cdls(dd[0])
    print(dd[1])
    for ii, data in enumerate(res_cdls):
        if data != 0: print(stock_code, dd[1], datas.index[ii].date(), data)

# # 计算指标
# crows2 = ti.cdls('CDL2CROWS')
# crows3 = ti.cdls('CDL3BLACKCROWS')
