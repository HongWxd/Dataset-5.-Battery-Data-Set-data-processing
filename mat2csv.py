import scipy.io
import numpy as np
import pandas as pd
import os
from Capacity_cal import Capacity_cal

def mat_to_csv(mat_folder):
    # 获取.mat文件夹中所有文件名
    mat_files = [f for f in os.listdir(mat_folder) if f.endswith('.mat')]

    for file in mat_files:
        # 构造.mat文件的完整路径
        mat_file_path = os.path.join(mat_folder, file)

        # 加载.mat文件
        mat_data = scipy.io.loadmat(mat_file_path)

        # 获取需要转换的数据
        cycles = mat_data[file.split('.')[0]]['cycle'][0, 0]

        # 创建空DataFrame
        data = pd.DataFrame()

        # 初始化循环计数
        cycle_count = 0
        cycle_charge = 0
        prev_cycle_type = None

        # 遍历循环数据
        for i in range(cycles.shape[1]):
            cycle = cycles[0, i]
            print("轮数:", i)
            # 处理charge类型的数据
            if cycle['type'][0] == 'charge':
                cycle_count += 1  # 只有在遍历到'charge'类型时才增加cycle计数
                cycle_charge = cycle_count
                prev_cycle_type = 'charge'
            # 处理discharge类型的数据
            elif cycle['type'][0] == 'discharge':
                cycle_count = cycle_charge  # 只有在遍历到'discharge'类型时才增加cycle计数
                prev_cycle_type = 'discharge'
            # 处理impedance类型的数据
            elif cycle['type'][0] == 'impedance':
                # 如果前一个类型是charge或discharge，则使用其cycle值，否则cycle值不变
                if prev_cycle_type in ['charge', 'discharge']:
                    cycle_count = cycle_count
                else:
                    cycle_count = cycle_count + 1
                prev_cycle_type = 'impedance'

            cycle_data = cycle['data'][0, 0]
            cycle_dict = {
                'Type': cycle['type'][0],
                'Cycle': cycle_count
            }

            if cycle['type'][0] == 'charge':
                cycle_dict['Voltage_measured(V)'] = cycle_data['Voltage_measured'][0]
                cycle_dict['Current_measured(Amps)'] = cycle_data['Current_measured'][0]
                cycle_dict['Temperature_measured(degree C)'] = cycle_data['Temperature_measured'][0]
                cycle_dict['Current_charge(Amps)'] = cycle_data['Current_charge'][0]
                cycle_dict['Voltage_charge(V)'] = cycle_data['Voltage_charge'][0]
                cycle_dict['Time(s)'] = cycle_data['Time'][0]

            elif cycle['type'][0] == 'discharge':
                cycle_dict['Voltage_measured(V)'] = cycle_data['Voltage_measured'][0]
                cycle_dict['Current_measured(Amps)'] = cycle_data['Current_measured'][0]
                cycle_dict['Temperature_measured(degree C)'] = cycle_data['Temperature_measured'][0]
                cycle_dict['Current_load(Amps)'] = cycle_data['Current_load'][0]
                cycle_dict['Voltage_load(V)'] = cycle_data['Voltage_load'][0]
                cycle_dict['Time(s)'] = cycle_data['Time'][0]
                if cycle_data['Capacity'][0].size > 0:  # 检查Capacity是否为空
                    cycle_dict['Capacity(Ahr)'] = [cycle_data['Capacity'][0][0]] * len(cycle_data['Time'][0])
                else:
                    cycle_dict['Capacity(Ahr)'] = [0] * len(cycle_data['Time'][0])

            elif cycle['type'][0] == 'impedance':
                # 转置 'Battery_impedance' 和 'Rectified_Impedance' 的数组，使其变为 1*48 形式
                battery_impedance = cycle_data['Battery_impedance'].T
                rectified_impedance = cycle_data['Rectified_Impedance'].T

                # 将 Rectified_Impedance 扩展为与 Battery_impedance 相同长度的数组
                if len(rectified_impedance[0]) < 48:
                    extra_length = 48 - len(rectified_impedance[0])
                    rectified_impedance_extended = np.append(rectified_impedance, [None] * extra_length)
                else:
                    rectified_impedance_extended = rectified_impedance[0]

                cycle_dict['Sense_current(Amps)'] = cycle_data['Sense_current'][0]
                cycle_dict['Battery_current(Amps)'] = cycle_data['Battery_current'][0]
                cycle_dict['Current_ratio'] = cycle_data['Current_ratio'][0]
                cycle_dict['Battery_impedance(0hms)]'] = battery_impedance[0]
                cycle_dict['Rectified_impedance(0hms)'] = rectified_impedance_extended
                cycle_dict['Re(0hms)'] = [cycle_data['Re'][0][0]] * 48
                cycle_dict['Rct(0hms)'] = [cycle_data['Rct'][0][0]] * 48

            temp_df = pd.DataFrame(cycle_dict)
            data = pd.concat([data, temp_df], ignore_index=True)

        # 将DataFrame写入CSV文件，文件名与.mat文件相同，但扩展名为.csv
        csv_file_path = os.path.join(mat_folder, file.split('.')[0] + '.csv')
        data.to_csv(csv_file_path, index=False)

# 调用函数并指定.mat文件所在的文件夹路径
'''

'''
if __name__ == "__main__":
    # 将mat文件转为csv文件
    mat_folder_path = 'D:\Program\mat2csv\F'
    mat_to_csv(mat_folder_path)

    # 计算csv文件中charge和discharge情况下的Capacity数据
    Capacity_cal(mat_folder_path)


