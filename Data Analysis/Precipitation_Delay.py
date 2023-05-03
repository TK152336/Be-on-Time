# 匯入所需套件
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
sns.set_palette('pastel')
sns.set_style('darkgrid')
%config inlineBackend.figure_format = 'retina'

# 航班+天氣母檔讀進來
precipitation_Delay_pt = pd.read_csv('../US_1722_flights_dataset_IQR.csv',usecols=['airline','flight_num','tail_num','airport_depa','airport_dest','year_sche_depa','month_sche_depa','day_sche_depa','hr_sche_depa','min_sche_depa','actu_duration','delay_duration','delay_depa','delay_dest','delay_weather','state_depa','state_dest','airport_depa','state_dest','precipitation_depa','precipitation_dest'])

# 將空值去除
precipitation_Delay_pt = precipitation_Delay_pt.dropna()

# 把delay分級級距
bins = [-np.inf, 5, 10, 15, 20, 25, 30, np.inf]
precipitation_Delay_pt['delay_depa_cate'] = pd.cut(precipitation_Delay_pt['delay_dest'], bins=bins, labels=[0, 1, 2, 3, 4, 5, 6])

# 取得出勤航班
# 篩掉取消航班，留下真的有飛的航班
precipitation_Delay_pt = precipitation_Delay_pt[precipitation_Delay_pt['actu_duration'] != 0]

# 觀察資料整體分布情況
sns.kdeplot(data=precipitation_Delay_pt[['precipitation_dest']], x="precipitation_dest" )
plt.savefig('16_0.Snow_fall_dest_distribution_0417.png')

# 繪圖
#設定畫布大小
plt.figure(figsize=(18, 10))

#設定圖表標頭
plt.title('16.Precipitation_Delay',fontsize=20)

# 設置漸層色彩
plt.tick_params(axis='y', which='both', labelsize=15)
plt.tick_params(axis='x', which='both', labelsize=15)

plt.scatter(data = precipitation_Delay_pt , x="delay_dest" , y="precipitation_dest"  ,alpha=0.3)
plt.xticks(ticks=[-50,-40,-30,-20,-10,0,10,20,30,40] ,labels=['-50','-40','-30','-20','-10','0','10','20','30','40'] ,minor=False)
plt.xlim(-50, 40)

plt.xlabel('Delay_mins',fontsize=15)
plt.ylabel('Precipitation_Delay',fontsize=15)

# 將圖表出以.png檔存出來
plt.savefig('16.Precipitation_Delay_whole_0417.png')