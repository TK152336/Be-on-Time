import pandas as pd
import os
import shutil
import numpy as np

# step1讀入機場與氣象站mapping檔 並預先設定好WBAN碼型態為 '字串' (456 rows × 5 columns)
df= pd.read_csv('../airport_機場/研究結果/airport_info_0321.csv',dtype={2:'str'})

# step2列出爬取到的所有天氣站觀測資訊檔案清單 (2216 筆)
weat_stat=[]
weat_stat= os.listdir('C:/Users/terra/BDSE29_learning data/期末專題/3.期末/資料研究/weather_天氣/02_fp_data_weather2')

#把氣象站清單從list轉成dataframe 以利後續使用 (2216 rows × 1 columns)
df_wea= pd.DataFrame(weat_stat)

# step3把天氣站觀測資訊檔案檔名中的"WBAN"抓出來 並新增此一"WBAN"欄位  (2216 rows × 2 columns)
df_wea['WBAN']=[x[13:18] for x in weat_stat]

# step4 合併兩表 df_wea(大) df(小) 以小表為主(right) 以此篩選出我們所需的 機場氣象觀測站 
# 456[-13]-9-1=446 (446 rows × 6 columns)
WBAN_mapping = pd.merge(df_wea, 
                     df, 
                     on = "WBAN",
                     how ='right')

# !檢查!有無沒有對應到的觀測站點
aa=WBAN_mapping[WBAN_mapping[0].isna()]
aa.to_excel('沒有爬到對應的氣象站點_0327.xlsx',index=None,encoding='utf-8')

# step5 檢查當中空值 (有9筆偏遠奇怪停用機場找不到氣象站可對應 1筆為純軍機場) 所以予以刪除該樣本
WBAN_mapping.isna().sum()

# 刪除後的新變數 WBAN_mapping_new
WBAN_mapping_new=WBAN_mapping.dropna(axis=0,how='any')

# step6 把mapping到的氣象站觀測資料檔案 複製到另一個資料夾予以區別
src='C:/Users/terra/BDSE29_learning data/期末專題/3.期末/資料研究/weather_天氣/02_fp_data_weather2/'
dst='C:/Users/terra/BDSE29_learning data/期末專題/3.期末/資料研究/weather_天氣/'
if not os.path.exists(f'{dst}airport_weather_stat'):
    os.makedirs(f'{dst}airport_weather_stat')

for i in WBAN_mapping_new[0]:
    shutil.copy2(f'{src}{i}', \
                f'{dst}airport_weather_stat')

# step7 把mapping過程都另存出來留存備查

# 機場第一次與天氣站點核對
WBAN_mapping.to_excel('WBAN_mapping.xlsx',index=None,encoding='utf-8')
# 清整完na後最終版
WBAN_mapping_new.to_excel('WBAN_mapping_new.xlsx',index=None,encoding='utf-8')
# 實際會用到的天氣站點446-22(機場名字重複，實則為同一機場，同一觀測站) =424
a=os.listdir('C:\\Users\\terra\\BDSE29_learning data\\期末專題\\3.期末\\資料研究\\weather_天氣\\airport_weather')
airport_weather=pd.DataFrame(a)
airport_weather.to_excel('airport_weather.xlsx',encoding='utf-8')












    
