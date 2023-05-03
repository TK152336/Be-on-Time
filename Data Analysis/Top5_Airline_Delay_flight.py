# 匯入所需套件
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_palette('pastel')
sns.set_style('whitegrid')
%config inlineBackend.figure_format = 'retina'

# 讀進航班母檔 
EDA_pt = pd.read_csv('../US_1722_flights_info_IQR.csv', usecols=['actu_duration','airline','flight_num','tail_num','delay_duration','delay_depa','delay_dest','year_sche_depa','airport_depa','state_depa','airport_dest','state_dest'])

# 取得出勤航班
# 篩掉取消航班，留下真的有飛的航班
EDA_pt_act = EDA_pt[EDA_pt['actu_duration'] != 0]

# 取得delay航班數
# 先篩選出有delay的出勤航班 再以航班分組
delay_counts = EDA_pt_act [EDA_pt_act ['delay_dest'] > 5].groupby(['airline','airport_depa','airport_dest']).count()[['tail_num']]
delay_counts =delay_counts.reset_index(drop=False)

# 為了計算誤點率 將總航班量、誤點量兩表合併
delay_counts_pt = pd.merge(
    total_flights,
    delay_counts,
    left_on= ['airline','airport_depa','airport_dest'],
    right_on=['airline','airport_depa','airport_dest'],
    how= 'left',
    suffixes=('_total_flights','_delay_flights')
)

delay_counts_pt['tail_num_delay_flights'] = delay_counts_pt['tail_num_delay_flights'].fillna(0)

# 計算誤點率
# 計算每條航班的誤點率 該航班誤點數 / 該航班出勤數 並把誤點率從高至低排序
delay_counts_pt['delay_rates'] = delay_counts_pt['tail_num_delay_flights'] / delay_counts_pt['tail_num_total_flights']
delay_counts_pt = delay_counts_pt.sort_values(by= 'delay_rates',ascending=False)

# 將誤點率極端值排除 並篩選出前5大航空業者的資料
delay_counts_pt_plt = delay_counts_pt[(delay_counts_pt['delay_rates']<1) & (delay_counts_pt['delay_rates']>0)]
delay_counts_pt_plt['flight_name'] = delay_counts_pt_plt[['airport_depa','airport_dest']].apply(lambda x : '-'.join(x), axis=1)
filt_value = ['WN','DL','AA','OO','UA']
filt = delay_counts_pt_plt["airline"].isin(filt_value)
Top5_airline_delay_rates_out = delay_counts_pt_plt[filt]

# 選出5間航空公司皆有營運的10條航線 用航線groupby後記數為5者
Top5_airline_byflight = Top5_airline_delay_rates_out.groupby(['flight_name']).count()[['delay_rates']]
Top5_airline_byflight_mutual = Top5_airline_byflight[Top5_airline_byflight['delay_rates']==5]
Top5_airline_byflight_mutual = Top5_airline_byflight_mutual.reset_index(drop=False)
Top5_airline_byflight_mutual_10 = Top5_airline_byflight_mutual.iloc[0:10,:]
Top5_airline_byflight_mutual_10

# 將5間航空公司皆有營運的10條航線 與 誤點率大表合併 再篩選出前5大航空業者 得出"前大航空業者 皆有營運的航線的誤點率比較"
airline_byflight_mutual = pd.merge(
    Top5_airline_byflight_mutual_10,
    delay_counts_pt_plt,
    left_on='flight_name',
    right_on='flight_name',
    how='left',
    suffixes=('_flight','_airline')
)
filt_value = ['WN' ,'DL' ,'AA','OO','UA']
filt = airline_byflight_mutual["airline"].isin(filt_value)
Top5_airline_delay_rates_mutual = airline_byflight_mutual[filt]

# 繪圖
#設定畫布大小
plt.figure(figsize=(12, 8))

#設定圖表標頭
plt.title('2.Top5_Airline_Delay_flight',fontsize=20)

plt.yticks(np.linspace(0,0.25,6),minor=False)
plt.ylim(0, 0.25)
plt.tick_params(axis='y', which='both', labelsize=13)
plt.tick_params(axis='x', which='both', labelsize=13)

ax = sns.scatterplot(Top5_airline_delay_rates_mutual , x="flight_name" , y="delay_rates_airline", hue='airline' ,palette="Greens_d",style="airline" , s=200 )

ax.set_xlabel('Flight_Name',fontsize=13)
ax.set_ylabel('Delay_Rates',fontsize=13)

handles, labels = plt.gca().get_legend_handles_labels()
plt.legend(handles, labels, fontsize=15,markerscale=3,loc='upper left')

# 將圖表出以.png檔存出來
plt.savefig('2.Top5_Airline_Delay_flight_0423.png')