# 匯入所需套件
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set_palette('pastel')
sns.set_style('whitegrid')
%config inlineBackend.figure_format = 'retina'\

# 讀進航班、天氣母檔 
EDA_pt = pd.read_csv('../US_1722_flights_dataset_IQR.csv', usecols=['airline','flight_num','tail_num','airport_depa','airport_dest','year_sche_depa','month_sche_depa','day_sche_depa','hr_sche_depa','min_sche_depa','actu_duration','delay_duration','delay_depa','delay_dest','delay_weather','state_depa','state_dest','airport_depa','state_dest','wind_dict_dest','wind_speed_dest'])

# 將空值去除
Wind_speed_Delay = EDA_pt.dropna()

# 取得出勤航班
# 篩掉取消航班，留下真的有飛的航班
Wind_speed_Delay = Wind_speed_Delay[Wind_speed_Delay['actu_duration'] != 0]

# 觀察資料整體分布情況
sns.kdeplot(data=Wind_speed_Delay[['wind_speed_dest']], x="wind_speed_dest" )
plt.show()
plt.savefig('17_0.Wind_speed_distribution_0416.png')

# 抓取繪圖會需要的欄位
Wind_speed_Delay_plt= Wind_speed_Delay[['delay_dest','wind_speed_dest','state_dest']]

# 繪圖
#以seaborn 劃出分點散布圖
#設定畫布大小
plt.figure(figsize=(18, 10))

#設定圖表標頭
plt.title('17.Wind_speed_Delay',fontsize=20)

plt.scatter(data=Wind_speed_Delay_plt , x="delay_dest" , y="wind_speed_dest" ,alpha=0.23)
plt.tick_params(axis='y', which='both', labelsize=15)
plt.yticks(np.linspace(0, 90,7),minor=False)
plt.ylim(0, 90)

plt.tick_params(axis='x', which='both', labelsize=15)
plt.xticks(ticks=[-50,-40,-30,-20,-10,0,10,20,30,40] ,labels=['-50','-40','-30','-20','-10','0','10','20','30','40'] ,minor=False)
plt.xlim(-50, 40)
plt.xlabel('Delay_mins',fontsize=15)
plt.ylabel('Wind_speed',fontsize=15)

# 將圖表出以.png檔存出來
plt.savefig('17.Wind_speed_Delay_0417_whole.png')