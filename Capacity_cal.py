# import pandas as pd
# from scipy.integrate import trapz
# import glob
#
# def Capacity():
#     # 指定多个文件夹路径
#     folder_paths = [ 'D/', 'E/', 'F/']
#
#     # 循环处理每个文件夹
#     for folder_path in folder_paths:
#         # 遍历指定文件夹下的所有CSV文件
#         csv_files = glob.glob(folder_path + '*.csv')
#
#         # 循环处理每个CSV文件
#         for file in csv_files:
#             # 读取CSV文件
#             df = pd.read_csv(file)
#
#             # 将时间单位转换为小时
#             df['Time(hr)'] = df['Time(s)'] / 3600
#
#             # 深拷贝一份 Capacity 列数据用于后续合并
#             df['Original_Capacity(Ahr)'] = df['Capacity(Ahr)'].copy()
#
#             # 循环处理每个轮数的 charge 数据
#             for cycle_num, cycle_group in df[df['Type'] == 'charge'].groupby('Cycle'):
#                 capacity_values = []
#                 for i in range(len(cycle_group)):
#                     print("轮数:", i)
#                     # 对每个时刻进行积分计算得到 Capacity 值
#                     sub_cycle_group = cycle_group.iloc[:i + 1]
#                     capacity = trapz(sub_cycle_group['Current_charge(Amps)'], sub_cycle_group['Time(hr)'])
#                     capacity_values.append(capacity)
#                 cycle_group['Capacity(Ahr)'] = capacity_values
#                 df.loc[cycle_group.index, 'Capacity(Ahr)'] = cycle_group['Capacity(Ahr)']
#
#             # 合并 charge 和非 charge 类型的 capacity 数据
#             df['Capacity(Ahr)'] = df['Capacity(Ahr)'].combine_first(df['Original_Capacity(Ahr)'])
#             df = df.drop(columns=['Original_Capacity(Ahr)'])  # 删除中间列 Original_Capacity(Ahr)
#
#             # 保存结果回原始CSV文件中
#             df.to_csv(file, index=False)
#
# # 调用函数执行处理
# Capacity()

import pandas as pd
import glob
from scipy.integrate import trapz

def Capacity_cal(folder_path):
    # 获取文件夹中所有CSV文件路径
    file_paths = glob.glob(folder_path + '/*.csv')

    for file_path in file_paths:
        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 将时间单位转换为小时
        df['Time(hr)'] = df['Time(s)'] / 3600

        # 循环处理每个轮数的 charge 和 discharge 数据
        for cycle_num, cycle_group in df.groupby(['Cycle', 'Type']):
            capacity_values = []
            for i in range(len(cycle_group)):
                sub_cycle_group = cycle_group.iloc[:i + 1]
                capacity = trapz(sub_cycle_group['Current_measured(Amps)'], sub_cycle_group['Time(hr)'])
                if cycle_group['Type'].iloc[0] == 'charge':
                    print("charge 轮数:", i)
                    capacity = max(0, capacity)  # 如果是charge类型且capacity为负数，用0来代替
                elif cycle_group['Type'].iloc[0] == 'discharge':
                    print("discharge 轮数:", i)
                    capacity = min(0, capacity)  # 如果是discharge类型且capacity为正数，用0来代替
                capacity_values.append(capacity)
            cycle_group['Capacity(Ahr)'] = capacity_values
            df.loc[cycle_group.index, 'Capacity(Ahr)'] = cycle_group['Capacity(Ahr)']

        # 保存结果回原始CSV文件中（覆盖原文件）
        df.to_csv(file_path, index=False)

    print("所有CSV文件处理完成。")


