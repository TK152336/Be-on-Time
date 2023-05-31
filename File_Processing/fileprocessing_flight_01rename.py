import pandas as pd
import os
from os import walk
from os.path import join

# 指定存放檔案目錄路徑
dir_path = 'C:/Users/Cheng/topic/final_data'

# add list save all file path
all_file_path = []

# 遞迴列出所有檔案的絕對路徑
for root, dirs, files in walk(dir_path):
    for f in files:
        all_file_path.append(join(root, f))


# 依序讀取所有csv文件
for file_name in all_file_path:

    # 抓檔名
    #指定哪幾列
    specific_rows = [1,2,5]
    df = pd.read_csv(f'{file_name}', skiprows = lambda x: x not in specific_rows,sep=',',header=None)

    # 拿來放檔名的list
    fn=[]
    # 抓出年分
    yr = df.iloc[2, 0].split(':')[-1][-2:]
    fn.append(yr)
    # 抓出機場代碼
    # punctuation= '()'
    airport = df.iloc[0,1].split(' ')[-1].strip('()')
    fn.append(airport)
    # 抓出航空公司代碼
    # punctuation= '()'
    airline = df.iloc[1,0].split(' ')[-1].strip('()')
    fn.append(airline)
    # 把年分、機場代碼、航空公司代碼組合
    filename='_'.join(fn)

    # 讀檔案，只讀我需要的部分
    # 跳掉前7列不要讀
    df1 = pd.read_csv(f'{file_name}', skiprows = [i for i in range (0,7)])
    
    # 刪掉最後一列，並且要直接刪原檔，不是view 是copy
    df1.drop(df1.tail(1).index,inplace=True)
    
    # 新增起飛機場欄位，在目的地機場的後面
    col_name = df1.columns.tolist()
    col_name.insert(col_name.index('Destination Airport')+1, 'Departure airport')
    df1 = df1.reindex(columns=col_name)
    df1['Departure airport'] = airport

    # 令存新檔，存出來
    # 建立目錄
    folderPath = 'Data_preprocessings'
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    #寫出檔案 不要標頭 不要index
    df1.to_csv(f'{folderPath}/flight_info_{filename}.csv',index=None)
