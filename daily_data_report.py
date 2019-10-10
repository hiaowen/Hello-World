#coding:utf-8

import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
import pymysql
import matplotlib.dates as mdate  # 用于设置日期格式
import matplotlib
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Scatter
from pyecharts import Gauge
from pyecharts import Funnel
from pyecharts import Geo
from pyecharts import WordCloud
from pyecharts import Line, Grid
from pyecharts import Overlap
from pyecharts import Page
from pyecharts import Radar
from sqlalchemy import create_engine

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Mac系统下设置matplotlib显示中文
plt.rcParams["font.family"] = 'Arial Unicode MS'
# 打印时显示出dataframe的全部列
pd.options.display.max_columns=999

# ==================== 将远端数据库的最新数据同步到本地数据库和excel表 ====================

# 通过pymysql方式连接远端数据库
remotedb = pymysql.connect(
    host="240c:f:1:6000::575f",
    port=3306,
    user="root",
    password="123456",
    database="internet_data"
    )
remotecur = remotedb.cursor()
print('通过pymysql方式连接远端数据库成功！', '\n')

# 通过create_engine方式连接本地数据库
engine_local = create_engine('mysql+pymysql://root:chenhiaowen@localhost:3306/workdata')
print('通过create_engine方式连接本地数据库成功！', '\n')

# 通过pymysql方式连接本地数据库
localdb = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="chenhiaowen",
    database="workdata",
    charset='utf8'
)
localcur = localdb.cursor()
print('通过pymysql方式连接本地数据库成功！', '\n')

# -------------------- 取本地数据库monitor_daily数据 --------------------
sql_m = "select * from monitor_daily"
df_m = pd.read_sql(sql_m, con=localdb)
df_m = df_m.sort_values(by='日期')
df_m = df_m.set_index('日期')
print('读取本地数据库monitor_daily表成功！','\n')

# -------------------- 同步capacity_daily数据 --------------------
sql_c = "select * from capacity_daily"
df_c = pd.read_sql(sql_c,con=remotedb)
df_c = df_c.sort_values(by='time')
df_c = df_c.set_index('time')
print('读取远端数据库capacity_daily表成功！','\n')

# 【方案1】capacity_daily整表同步到本地
# 新生成一张excel表，直接覆盖本机电脑上的原表
df_c.to_excel('/Users/czx/我的坚果云/Learn/Python/workdata/capacity_daily.xlsx',index=True)
print('生成新的capacity_daily.xlsx，并替换原表（如有），保存成功！')
# 新生成一个table表，直接覆盖本地数据库的原表
# 初始化本地数据库连接，使用pymysql模块
# 将新建的DataFrame储存为MySQL中的数据表，不储存index列
df_c.to_sql('capacity_daily', con=engine_local, if_exists='replace', index=True)
print('创建本地数据库capacity_daily表，并替换原表（如有），保存成功！')
# 【方案2】只将新增数据同步到本地
# 将最新的记录增加到到已有的excel表里
# wb = load_workbook('/Users/czx/我的坚果云/Learn/Python/workdata/capacity_daily.xlsx')
# ws = wb.worksheets[0]
# for n in range(0,3):
#     ws.append(list(df_c.tail(3).iloc[n,:]))
# wb.save('/Users/czx/我的坚果云/Learn/Python/workdata/capacity_daily.xlsx')
# print('在本机现有capacity_daily.xlsx表中增加记录成功!','\n')
# 将最新记录数据写入本地数据库已有表
# df_c = df_c.tail(3)
# for n in range(0,3):
#     sql_c_addnew = "INSERT INTO capacity_daily VALUES(%s,'%s','%s',%s,%s,%s,%s,%s,%s,%s,%s)"%(df_c.iloc[n,0],df_c.iloc[n,1],df_c.iloc[n,2],df_c.iloc[n,3],df_c.iloc[n,4],df_c.iloc[n,5],df_c.iloc[n,6],df_c.iloc[n,7],df_c.iloc[n,8],df_c.iloc[n,9],df_c.iloc[n,10])
#     localcur.execute(sql_c_addnew)
#     localdb.commit()
# print("新记录写入本地数据库capacity_daily表成功！")


# -------------------- 同步其他数据 --------------------
# capacity_daily_ipman_c2p整表同步到本地
sql_c_ipman_c2p = "select * from capacity_daily_ipman_c2p"
df_c_ipman_c2p = pd.read_sql(sql_c_ipman_c2p,con=remotedb)
df_c_ipman_c2p = df_c_ipman_c2p.sort_values(by='time')         # 按日期进行排序
df_c_ipman_c2p = df_c_ipman_c2p.set_index('time')
print('远端数据库capacity_daily_ipman_c2p表读取成功！','\n')
# 新生成一张excel表，直接覆盖本机电脑上的原表
df_c_ipman_c2p.to_excel('/Users/czx/我的坚果云/Learn/Python/workdata/capacity_daily_ipman_c2p.xlsx',index=True)
print('生成新的capacity_daily_ipman_c2p.xlsx，并替换原表（如有），保存成功！')
# 新生成一个table表，直接覆盖本地数据库的原表
# 初始化本地数据库连接，使用pymysql模块
# 将新建的DataFrame储存为MySQL中的数据表，不储存index列
df_c_ipman_c2p.to_sql('capacity_daily_ipman_c2p', con=engine_local, if_exists='replace', index=True)
print('创建本地数据库capacity_daily_ipman_c2p表，并替换原表（如有），保存成功！')

# capacity_daily_ipman_c2b整表同步到本地
sql_c_ipman_c2b = "select * from capacity_daily_ipman_c2b"
df_c_ipman_c2b = pd.read_sql(sql_c_ipman_c2b,con=remotedb)
df_c_ipman_c2b = df_c_ipman_c2b.sort_values(by='time')
df_c_ipman_c2b = df_c_ipman_c2b.set_index('time')
print('远端数据库capacity_daily_ipman_c2b表读取成功！','\n')
# 新生成一张excel表，直接覆盖本机电脑上的原表
df_c_ipman_c2b.to_excel('/Users/czx/我的坚果云/Learn/Python/workdata/capacity_daily_ipman_c2b.xlsx',index=True)
print('生成新的capacity_daily_ipman_c2b.xlsx，并替换原表（如有），保存成功！')
# 新生成一个table表，直接覆盖本地数据库的原表
# 初始化本地数据库连接，使用pymysql模块
# 将新建的DataFrame储存为MySQL中的数据表，不储存index列
df_c_ipman_c2b.to_sql('capacity_daily_ipman_c2b', con=engine_local, if_exists='replace', index=True)
print('创建本地数据库capacity_daily_ipman_c2b表，并替换原表（如有），保存成功！')

# capacity_daily_cmnet_c2p整表同步到本地
sql_c_cmnet_c2p = "select * from capacity_daily_cmnet_c2p"
df_c_cmnet_c2p = pd.read_sql(sql_c_cmnet_c2p,con=remotedb)
df_c_cmnet_c2p = df_c_cmnet_c2p.sort_values(by='time')         # 按日期进行排序
df_c_cmnet_c2p = df_c_cmnet_c2p.set_index('time')
print('远端数据库capacity_daily_cmnet_c2p表读取成功！','\n')
# 新生成一张excel表，直接覆盖本机电脑上的原表
df_c_cmnet_c2p.to_excel('/Users/czx/我的坚果云/Learn/Python/workdata/capacity_daily_cmnet_c2p.xlsx',index=True)
print('生成新的capacity_daily_cmnet_c2p.xlsx，并替换原表（如有），保存成功！')
# 新生成一个table表，直接覆盖本地数据库的原表
# 初始化本地数据库连接，使用pymysql模块
# 将新建的DataFrame储存为MySQL中的数据表，不储存index列
df_c_cmnet_c2p.to_sql('capacity_daily_cmnet_c2p', con=engine_local, if_exists='replace', index=True)
print('创建本地数据库capacity_daily_cmnet_c2p表，并替换原表（如有），保存成功！')

# -------------------- 同步flow_daily数据 --------------------
sql_f="select * from flow_daily"
df_f = pd.read_sql(sql_f,con=remotedb)
df_f = df_f.sort_values(by='time')
print('读取远端数据库flow_daily表成功！')
# print(df_f.columns)
df_f.columns=['date','allflow_inIPTV_PB','allflow_exIPTV_PB','IPTV_PB','jiakuan_PB','zhuanxian_PB','localrate','down_to_city_Gbps','bbinternetwork_mean_Gbps','bbinternation_mean_Gbps','NAP_mean_Gbps','bbinternetwork_peak_Gbps','IPTVlive_Gbps','down_to_city_exIPTVlive_Gbps','IPTV_exlive_Gbps','NAP_true_mean_Gbps']
# print(df_f.tail(1))

# 【方案1】flow_daily整表同步到本地
# 新生成一张excel表，直接覆盖本机电脑上的原表
df_f.to_excel('/Users/czx/我的坚果云/Learn/Python/workdata/flow_daily.xlsx',index=False)
print('生成新的flow_daily.xlsx，并替换原表（如有），保存成功！')
# 新生成一个table表，直接覆盖本地数据库的原表
# 初始化本地数据库连接，使用pymysql模块
# 将新建的DataFrame储存为MySQL中的数据表，不储存index列
df_f.to_sql('flow_daily', con=engine_local, if_exists='replace', index=False)
print('创建本地数据库flow_daily表，并替换原表（如有），保存成功！')
# 【方案2】只将新增数据同步到本地
# 将最新的一行记录增加到到已有的excel表里
# new_data = list(df_f.iloc[-1,:])
# wb = load_workbook('/Users/czx/我的坚果云/Learn/Python/workdata/flow_daily.xlsx')
# ws = wb.worksheets[0]
# ws.append(new_data)
# wb.save('/Users/czx/我的坚果云/Learn/Python/workdata/flow_daily.xlsx')
# 将最新记录写入本地数据库已有表
# sql_f_addnew = "INSERT INTO flow_daily VALUES('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"%(df_f.iloc[-1,:][0],df_f.iloc[-1,:][1],df_f.iloc[-1,:][2],df_f.iloc[-1,:][3],df_f.iloc[-1,:][4],df_f.iloc[-1,:][5],df_f.iloc[-1,:][6],df_f.iloc[-1,:][7],df_f.iloc[-1,:][8],df_f.iloc[-1,:][9],df_f.iloc[-1,:][10],df_f.iloc[-1,:][11],df_f.iloc[-1,:][12],df_f.iloc[-1,:][13],df_f.iloc[-1,:][14],df_f.iloc[-1,:][15])
# print('在本机现有flow_daily.xlsx表中增加记录成功!','\n')
# localcur.execute(sql_f_addnew)
# localdb.commit()
# print("新记录写入本地数据库flow_daily表成功！")

localdb.close()
remotedb.close()


# ==================== 制作pyecharts多图 ====================

page = Page()

df_f_recent = df_f.tail(20)
df_f_recent = df_f_recent.set_index('date')

# 图1：家宽及专线流量柱状趋势图
overlap1 = Overlap()
bar1 = Bar('近期业务流量','单位：PB/天')
bar1.add('家宽bar', df_f_recent.index, df_f_recent['jiakuan_PB'], mark_point=["max", "min"], is_label_show=True)
bar1.add('专线bar', df_f_recent.index, df_f_recent['zhuanxian_PB'], mark_point=["max", "min"])
bar1.add('IPTVbar', df_f_recent.index, df_f_recent['IPTV_PB'], mark_point=["max", "min"])
line1 = Line('流量折线趋势图', '家宽&专线', title_top="45%")
line1.add('家宽line', df_f_recent.index, df_f_recent['jiakuan_PB'])
line1.add('专线line', df_f_recent.index, df_f_recent['zhuanxian_PB'])
line1.add('IPTVline', df_f_recent.index, df_f_recent['IPTV_PB'])
overlap1.add(bar1)
overlap1.add(line1)


# 图2：国际及网间流量折线趋势图
line2 = Line('国际&网间流量', '单位：Gbps')
line2.add('国际流量_全天均值', df_f_recent.index, df_f_recent['bbinternation_mean_Gbps'])
line2.add('网间流量_全天均值', df_f_recent.index, df_f_recent['bbinternetwork_mean_Gbps'], is_label_show=True)
line2.add('网间流量_忙时均值', df_f_recent.index, df_f_recent['bbinternetwork_peak_Gbps'], mark_point=["max", "min"], line_width=3)


# 图3：业务流量构成
df_m_yewu_latest = df_m[['家宽业务流量_TB','专线业务流量_TB','4G业务流量_TB','2G业务流量_TB']].tail(1)
attr = ['家宽', '专线', '4G', '2G']
# p1 = [11, 12, 14, 15, 10, 12]
pie = Pie('业务流量占比','单位：TB/天')
pie.add('', attr, df_m_yewu_latest.iloc[-1,:4], is_label_show=True)


# 图4：互联网业务总流量
overlap2 = Overlap()
df_m_yewu_recent = df_m[['家宽业务流量_TB','专线业务流量_TB','4G业务流量_TB','2G业务流量_TB','互联网业务总流量_TB']].tail(10)
bar2 = Bar('互联网业务总流量','单位：TB/天')
bar2.add('家宽',df_m_yewu_recent.index,df_m_yewu_recent['家宽业务流量_TB'].round(decimals=0),is_stack=True, mark_point=["max", "min"])
bar2.add('专线',df_m_yewu_recent.index,df_m_yewu_recent['专线业务流量_TB'],is_stack=True)
bar2.add('4G',df_m_yewu_recent.index,df_m_yewu_recent['4G业务流量_TB'],is_stack=True)
bar2.add('2G',df_m_yewu_recent.index,df_m_yewu_recent['2G业务流量_TB'],is_stack=True)
line3 = Line('总流量折线图', '家宽&专线&4G&2G', title_top="95%")
line3.add('总流量折线图', df_m_yewu_recent.index, df_m_yewu_recent['互联网业务总流量_TB'].round(decimals=0), mark_point=["max", "min"])
overlap2.add(bar2)
overlap2.add(line3)


# 图5：出口容量与利用率
# 只取各出口的数据
used_df_c = df_c[['省网上联国干出口','省网核心互联','NAP出口','铁通直连出口','IDC-省干出口','城域网-省干出口','城域网-国干出口','地市CMNET出口']]
# 最近一天的带宽数据
lastest_bw = used_df_c.iloc[0,:]
# 最近一天的峰值流量
lastest_flow_peak_in = used_df_c.iloc[1,:]
lastest_flow_peak_out = used_df_c.iloc[2,:]
df_c_join = pd.DataFrame([lastest_flow_peak_in, lastest_flow_peak_out])  # 将两个Series合并成一个Dataframe
lastest_flow_peak = df_c_join.max(axis=0)  # 两行数据比较取较大值
radar = Radar("出口带宽&利用率", "CMNET网络出口")
radar_data_max = [[lastest_flow_peak[0], lastest_flow_peak[1], lastest_flow_peak[2], lastest_flow_peak[3], lastest_flow_peak[4], lastest_flow_peak[5], lastest_flow_peak[6], lastest_flow_peak[7]]]
print(radar_data_max)
radar_data_in = [[lastest_flow_peak_in[0], lastest_flow_peak_in[1], lastest_flow_peak_in[2], lastest_flow_peak_in[3], lastest_flow_peak_in[4], lastest_flow_peak_in[5], lastest_flow_peak_in[6], lastest_flow_peak_in[7]]]
radar_data_out = [[lastest_flow_peak_out[0], lastest_flow_peak_out[1], lastest_flow_peak_out[2], lastest_flow_peak_out[3], lastest_flow_peak_out[4], lastest_flow_peak_out[5], lastest_flow_peak_out[6], lastest_flow_peak_out[7]]]
# radar_data_line = [[lastest_bw[0]*0.7, lastest_bw[1]*0.7, lastest_bw[2]*0.7, lastest_bw[3]*0.7, lastest_bw[4]*0.7, lastest_bw[5]*0.7, lastest_bw[6]*0.7, lastest_bw[7]*0.7]]
# 设置column的最大值
schema = [
    (used_df_c.columns[0], lastest_bw[0]*0.7), (used_df_c.columns[1], lastest_bw[1]*0.7), (used_df_c.columns[2], lastest_bw[2]*0.7),
    (used_df_c.columns[3], lastest_bw[3]*0.7), (used_df_c.columns[4], lastest_bw[4]*0.7), (used_df_c.columns[5], lastest_bw[5]*0.7),
    (used_df_c.columns[6], lastest_bw[6]*0.7), (used_df_c.columns[7], lastest_bw[7]*0.7)
]
# 传入坐标
radar.config(schema)
radar.add("max",radar_data_max, item_color='red',area_color="#ea3a2e",area_opacity=0.3,line_width=3, legend_top='bottom')
radar.add("in",radar_data_in, item_color='blue', legend_top='bottom')
radar.add("out",radar_data_out, item_color='green', legend_top='bottom')
# radar.add("line",radar_data_line, item_color='red')


# 图6：出口容量柱状图，利用率折线图
overlap3 = Overlap()
# 取最后一天的各出口的3个指标的数据，并转置，结果index为各出口名称，columns重命名为"带宽"，"流入峰值速率"，"流出峰值速率"，并按带宽排序
used_df_c = (used_df_c.tail(3)).T
used_df_c.columns=['带宽','流入峰值速率','流出峰值速率']
used_df_c_sort = used_df_c.sort_values(by='带宽',ascending=False)
"""
used_df_c_sort：
                带宽   流入峰值速率   流出峰值速率
IDC-省干出口   33620.0  7633.98  1284.48
城域网-省干出口   30720.0  3352.28  8612.60
地市CMNET出口  22530.0   656.52  4227.70
省网上联国干出口   12840.0  3353.98  1618.52
省网核心互联     12340.0  2864.61  3319.90
城域网-国干出口    3400.0   860.15   473.61
铁通直连出口       160.0    10.02     1.53
NAP出口         80.0     1.38     0.71
"""
# 取流速两列中数据大的数据组成新的列
lastest_flow_peak_col = used_df_c_sort[['流入峰值速率','流出峰值速率']].max(axis=1)
bar3 = Bar('出口容量&利用率')
bar3.add('峰值流速', used_df_c_sort.index, lastest_flow_peak_col, is_stack=True)
bar3.add('空闲带宽', used_df_c_sort.index, used_df_c_sort['带宽']-lastest_flow_peak_col, is_stack=True)
# 计算峰值利用率
latest_rate = lastest_flow_peak_col/used_df_c_sort['带宽']
line5 = Line('利用率折线图')
line5.add('峰值利用率', used_df_c_sort.index, (latest_rate*100).round(decimals=1), mark_point=['max'], yaxis_formatter="%", yaxis_interval=20)
overlap3.add(bar3)
overlap3.add(line5, yaxis_index=1, is_add_yaxis=True)


# 图7：网络出口流量趋势图
# 取不同指标名称的数据
df_c['城域网出口'] = df_c['城域网-省干出口'] + df_c['城域网-国干出口']
print(df_c)
df_c_bw = df_c[df_c['指标名称'] == '带宽(G)']
print(df_c_bw)
df_c_flow_in = df_c[df_c['指标名称'] == '流入峰值流速(Gbps)']
print(df_c_flow_in)
df_c_flow_out = df_c[df_c['指标名称'] == '流出峰值流速(Gbps)']
print(df_c_flow_out)
line4 = Line('网络出口流量','单位：Gbps')
line4.add("CMNET-BB_in", df_c_flow_in.index, df_c_flow_in['省网上联国干出口'].round(decimals=0), is_label_show=True, line_width=3, legend_top='bottom')
line4.add("CMNET-BB_out", df_c_flow_out.index, df_c_flow_out['省网上联国干出口'].round(decimals=0), is_label_show=True, legend_top='bottom')
line4.add("IPMAN_in", df_c_flow_out.index, df_c_flow_out['城域网出口'].round(decimals=0), is_label_show=True, line_width=3, legend_top='bottom')
line4.add("IPMAN_out", df_c_flow_in.index, df_c_flow_in['城域网出口'].round(decimals=0), legend_top='bottom')
line4.add("cityCMNET_in", df_c_flow_out.index, df_c_flow_out['地市CMNET出口'].round(decimals=0), is_label_show=True, line_width=3, legend_top='bottom')
line4.add("cityCMNET_out", df_c_flow_in.index, df_c_flow_in['地市CMNET出口'].round(decimals=0), legend_top='bottom')
line4.add("NAP_in", df_c_flow_in.index, df_c_flow_in['NAP出口'], is_label_show=True, line_width=3, legend_top='bottom')
line4.add("NAP_out", df_c_flow_out.index, df_c_flow_out['NAP出口'], legend_top='bottom')
line4.add("IDC_in", df_c_flow_out.index, df_c_flow_out['IDC-省干出口'], is_label_show=True, line_width=3, legend_top='bottom')
line4.add("IDC_out", df_c_flow_in.index, df_c_flow_in['IDC-省干出口'].round(decimals=0), legend_top='bottom')

# 图8：地市出口流量趋势图
df_c_ipman_c2p_guangzhou = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='广州城域网']
df_c_ipman_c2p_shenzhen = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='深圳城域网']
df_c_ipman_c2p_dongguan = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='东莞城域网']
df_c_ipman_c2p_foshan = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='佛山城域网']
df_c_ipman_c2p_shantou = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='汕头城域网']
df_c_ipman_c2p_zhuhai = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='珠海城域网']
df_c_ipman_c2p_huizhou = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='惠州城域网']
df_c_ipman_c2p_zhongshan = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='中山城域网']
df_c_ipman_c2p_jiangmen = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='江门城域网']
df_c_ipman_c2p_zhanjiang = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='湛江城域网']
df_c_ipman_c2p_maoming = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='茂名城域网']
df_c_ipman_c2p_jieyang = df_c_ipman_c2p[df_c_ipman_c2p['链路组']=='揭阳城域网']

df_c_ipman_c2b_guangzhou = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='广州城域网']
df_c_ipman_c2b_shenzhen = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='深圳城域网']
df_c_ipman_c2b_dongguan = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='东莞城域网']
df_c_ipman_c2b_foshan = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='佛山城域网']
df_c_ipman_c2b_shantou = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='汕头城域网']
df_c_ipman_c2b_zhuhai = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='珠海城域网']
df_c_ipman_c2b_huizhou = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='惠州城域网']
df_c_ipman_c2b_zhongshan = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='中山城域网']
df_c_ipman_c2b_jiangmen = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='江门城域网']
df_c_ipman_c2b_zhanjiang = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='湛江城域网']
df_c_ipman_c2b_maoming = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='茂名城域网']
df_c_ipman_c2b_jieyang = df_c_ipman_c2b[df_c_ipman_c2b['链路组']=='揭阳城域网']

df_c_ipman_guangzhou = pd.concat([df_c_ipman_c2p_guangzhou, df_c_ipman_c2b_guangzhou], axis=1)
df_c_ipman_guangzhou['peak_down'] = df_c_ipman_guangzhou.iloc[:,4] + df_c_ipman_guangzhou.iloc[:,10]
df_c_ipman_shenzhen = pd.concat([df_c_ipman_c2p_shenzhen, df_c_ipman_c2b_shenzhen], axis=1)
df_c_ipman_shenzhen['peak_down'] = df_c_ipman_shenzhen.iloc[:,4] + df_c_ipman_shenzhen.iloc[:,10]
df_c_ipman_dongguan = pd.concat([df_c_ipman_c2p_dongguan, df_c_ipman_c2b_dongguan], axis=1)
df_c_ipman_dongguan['peak_down'] = df_c_ipman_guangzhou.iloc[:,4] + df_c_ipman_dongguan.iloc[:,10]
df_c_ipman_foshan = pd.concat([df_c_ipman_c2p_foshan, df_c_ipman_c2b_foshan], axis=1)
df_c_ipman_foshan['peak_down'] = df_c_ipman_foshan.iloc[:,4] + df_c_ipman_foshan.iloc[:,10]
df_c_ipman_shantou = pd.concat([df_c_ipman_c2p_shantou, df_c_ipman_c2b_shantou], axis=1)
df_c_ipman_shantou['peak_down'] = df_c_ipman_shantou.iloc[:,4] + df_c_ipman_shantou.iloc[:,10]
df_c_ipman_zhuhai = pd.concat([df_c_ipman_c2p_zhuhai, df_c_ipman_c2b_zhuhai], axis=1)
df_c_ipman_zhuhai['peak_down'] = df_c_ipman_zhuhai.iloc[:,4] + df_c_ipman_zhuhai.iloc[:,10]
df_c_ipman_huizhou = pd.concat([df_c_ipman_c2p_huizhou, df_c_ipman_c2b_huizhou], axis=1)
df_c_ipman_huizhou['peak_down'] = df_c_ipman_huizhou.iloc[:,4] + df_c_ipman_huizhou.iloc[:,10]
df_c_ipman_zhongshan = pd.concat([df_c_ipman_c2p_zhongshan, df_c_ipman_c2b_zhongshan], axis=1)
df_c_ipman_zhongshan['peak_down'] = df_c_ipman_zhongshan.iloc[:,4] + df_c_ipman_zhongshan.iloc[:,10]
df_c_ipman_jiangmen = pd.concat([df_c_ipman_c2p_jiangmen, df_c_ipman_c2b_jiangmen], axis=1)
df_c_ipman_jiangmen['peak_down'] = df_c_ipman_jiangmen.iloc[:,4] + df_c_ipman_jiangmen.iloc[:,10]
df_c_ipman_zhanjiang = pd.concat([df_c_ipman_c2p_zhanjiang, df_c_ipman_c2b_zhanjiang], axis=1)
df_c_ipman_zhanjiang['peak_down'] = df_c_ipman_zhanjiang.iloc[:,4] + df_c_ipman_zhanjiang.iloc[:,10]
df_c_ipman_maoming = pd.concat([df_c_ipman_c2p_maoming, df_c_ipman_c2b_maoming], axis=1)
df_c_ipman_maoming['peak_down'] = df_c_ipman_maoming.iloc[:,4] + df_c_ipman_maoming.iloc[:,10]
df_c_ipman_jieyang = pd.concat([df_c_ipman_c2p_jieyang, df_c_ipman_c2b_jieyang], axis=1)
df_c_ipman_jieyang['peak_down'] = df_c_ipman_jieyang.iloc[:,4] + df_c_ipman_jieyang.iloc[:,10]



line6 = Line('城域网出口流量','单位：Gbps')
line6.add('GZ',df_c_ipman_guangzhou.index,df_c_ipman_guangzhou['peak_down'].round(decimals=0),line_width=3)
line6.add('SZ',df_c_ipman_shenzhen.index,df_c_ipman_shenzhen['peak_down'].round(decimals=0),line_width=3)
line6.add('DG',df_c_ipman_dongguan.index,df_c_ipman_dongguan['peak_down'].round(decimals=0),line_width=3)
line6.add('FS',df_c_ipman_foshan.index,df_c_ipman_foshan['peak_down'].round(decimals=0),line_width=3)
line6.add('ST',df_c_ipman_shantou.index,df_c_ipman_shantou['peak_down'].round(decimals=0))
line6.add('ZH',df_c_ipman_zhuhai.index,df_c_ipman_zhuhai['peak_down'].round(decimals=0))
line6.add('HZ',df_c_ipman_huizhou.index,df_c_ipman_huizhou['peak_down'].round(decimals=0))
line6.add('ZS',df_c_ipman_zhongshan.index,df_c_ipman_zhongshan['peak_down'].round(decimals=0))
line6.add('JM',df_c_ipman_jiangmen.index,df_c_ipman_jiangmen['peak_down'].round(decimals=0))
line6.add('ZJ',df_c_ipman_zhanjiang.index,df_c_ipman_zhanjiang['peak_down'].round(decimals=0))
line6.add('MM',df_c_ipman_maoming.index,df_c_ipman_maoming['peak_down'].round(decimals=0))
line6.add('JY',df_c_ipman_jieyang.index,df_c_ipman_jieyang['peak_down'].round(decimals=0))

print(df_c_ipman_c2p_guangzhou)

# 图9：关键指标仪表盘
gauge1 = Gauge('关键指标')
gauge1.add('业务指标', '流量本网率', df_f.tail(1)['localrate'])


page.add(overlap1)
page.add(line2)
page.add(pie)
page.add(overlap2)
page.add(radar)
page.add(overlap3)
page.add(line4)
page.add(line6)
page.add(gauge1)

page.render('/Users/czx/Desktop/data/alldata.html')

# print(df_c_ipman_guangzhou['peak_down'] )

# ---------------------自动发邮件-----------------------------------------------------------

# 设置smtplib所需的参数
# 下面的发件人，收件人是用于邮件传输的。
smtpserver = 'smtp.139.com'
username = 'hiaowen@139.com'
password = 'CHENxw26'
sender = 'hiaowen@139.com'
# receiver='XXX@126.com'
# 收件人为多个收件人
receiver = ['hiaowen@139.com', 'chenxiaowen6@gd.chinamobile.com']

subject = 'daily_data'
# 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
# subject = '中文标题'
# subject=Header(subject, 'utf-8').encode()

# 构造邮件对象MIMEMultipart对象
# 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
msg = MIMEMultipart('mixed')
msg['Subject'] = subject
msg['From'] = 'hiaowen@139.com <hiaowen@139.com>'
# msg['To'] = 'XXX@126.com'
# 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
msg['To'] = ";".join(receiver)
# msg['Date']='2012-3-16'


# 构造附件
sendfile = open(r'/Users/czx/Desktop/data/alldata.html', 'rb').read()
text_att = MIMEText(sendfile, 'base64', 'utf-8')
text_att["Content-Type"] = 'application/octet-stream'
# 以下附件可以重命名成aaa.txt
# text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
# 另一种实现方式
text_att.add_header('Content-Disposition', 'attachment', filename='alldata.html')
# 以下中文测试不ok
# text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
msg.attach(text_att)


# 发送邮件
smtp = smtplib.SMTP()
smtp.connect('smtp.139.com')
# 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
# smtp.set_debuglevel(1)
smtp.login(username, password)
smtp.sendmail(sender, receiver, msg.as_string())
smtp.quit()





# 合并数据表
# df_join = pd.concat([df_f, df_m], axis=1)
# # print(df_join)
# df_join.to_excel('/Users/czx/我的坚果云/Learn/Python/workdata/df_join.xlsx')