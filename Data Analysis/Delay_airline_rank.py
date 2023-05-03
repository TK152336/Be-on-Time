# 匯入所需套件
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set_palette('pastel')
sns.set_style('darkgrid')
%config inlineBackend.figure_format = 'retina'


# 讀進航班母檔
EDA_pt = pd.read_csv('../US_1722_flights_info_IQR.csv',usecols=['actu_duration','airline','flight_num','delay_duration','delay_depa','delay_dest','year_sche_depa'])

# 取得出勤航班
# 篩掉取消航班，留下真的有飛的航班
EDA_pt_act=EDA_pt[EDA_pt['actu_duration'] != 0]

# 取得出勤航班數
# 以航空公司分組，檢視每間航空公司實際出勤航班數
total_flights = EDA_pt_act.groupby('airline').count()[['flight_num']]
total_flights =total_flights.reset_index(drop=False)
total_flights_plt = total_flights.sort_values('flight_num',ascending=False)


#設置畫布
plt.figure(figsize=(12, 6))
plt.title('1_0.Total_Airlines_Rank')
plt.ticklabel_format(style='plain',axis='y')
#繪圖
ax = sns.barplot(data = total_flights_plt  , x="airline" , y="flight_num", palette="dark:#84C1FF" )
#將圖表出以.png檔存出來
plt.savefig('1_0.Total_Airlines_Rank_0416.png')