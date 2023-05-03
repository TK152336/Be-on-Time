# 匯入所需套件
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set_palette('pastel')
sns.set_style('whitegrid')
%config inlineBackend.figure_format = 'retina'

# 讀進航班、天氣母檔 
Wind_visibility_Delay_pt = pd.read_csv('../US_1722_flights_dataset_IQR.csv',usecols=['airline','flight_num','tail_num','airport_depa','airport_dest','year_sche_depa','month_sche_depa','day_sche_depa','hr_sche_depa','min_sche_depa','actu_duration','delay_duration','delay_depa','delay_dest','delay_weather','state_depa','state_dest','airport_depa','state_dest','visibility_dest'])

# 將空值去除
Wind_visibility_Delay_pt = Wind_visibility_Delay_pt.dropna()

# 把delay分級級距
bins = [-np.inf, 5, 10, 15, 20, 25, 30, np.inf]
Wind_visibility_Delay_pt['delay_depa_cate'] = pd.cut(Wind_visibility_Delay_pt['delay_dest'], bins=bins, labels=[0, 1, 2, 3, 4, 5, 6])

# 取得出勤航班
# 篩掉取消航班，留下真的有飛的航班
Wind_visibility_Delay_pt = Wind_visibility_Delay_pt[Wind_visibility_Delay_pt['actu_duration'] != 0]

# 取得出勤航班中有delay的
Wind_visibility_Delay_plt =  Wind_visibility_Delay_pt[(Wind_visibility_Delay_pt['delay_dest']>=5)&(Wind_visibility_Delay_pt['visibility_dest']<11)&(Wind_visibility_Delay_pt['visibility_dest']>9)]
Wind_visibility_Delay_plt = Wind_visibility_Delay_plt[['delay_dest','visibility_dest','delay_depa_cate']]

# 觀察資料整體分布情況
sns.kdeplot(data=Wind_visibility_Delay_plt[['visibility_dest']], x="visibility_dest" )
plt.savefig('18_0.Visibility_dest_distribution_0416.png')

# 繪圖
# 設定畫布大小
plt.figure(figsize=(18, 10))

# 設定圖表標頭
plt.title('18.Visibility_Delay',fontsize=20)

# 設置漸層色彩
plt.tick_params(axis='y', which='both', labelsize=15)
plt.tick_params(axis='x', which='both', labelsize=15)

plt.scatter(data = Wind_visibility_Delay_plt , x="delay_dest" , y="visibility_dest"  ,alpha=0.3)

plt.xticks(ticks=[-50,-40,-30,-20,-10,0,10,20,30,40] ,labels=['-50','-40','-30','-20','-10','0','10','20','30','40'] ,minor=False)
plt.xlim(-50, 40)

plt.xlabel('Delay_mins',fontsize=15)
plt.ylabel('Visibility_dest',fontsize=15)
plt.yticks(np.linspace(0,0.16,6),minor=False)
plt.ylim(0, 0.16)

# 將圖表出以.png檔存出來
plt.savefig('18.Visibility_whole_0421_1.png')

# 存出csv檔
Wind_visibility_Delay_plt.to_csv('18.Visibility_Delay_whole_0421.csv')