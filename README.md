# Dataset: 5.-Battery-Data-Set-data-processing
Dataset: Experiments on Li-Ion batteries. Charging and discharging at different temperatures. Records the impedance as the damage criterion. The data set was provided by the NASA Prognostics Center of Excellence (PCoE).
## mat2csv.py

- **作用：**mat2csv.py文件用于实现将数据集5.+Battery+Data+Set中提供的.mat数据文件转化为对应的.csv文件，并计算了charge和discharge情况下每一时刻对应的电池Capacity(Ahr)。
- **代码入口**

```python
if __name__ == "__main__":
    # 将mat文件转为csv文件
    mat_folder_path = 'D:\Program\mat2csv\F'
    mat_to_csv(mat_folder_path)

    # 计算csv文件中charge和discharge情况下的Capacity数据
    Capacity_cal(mat_folder_path)
```

执行不同文件夹中的数据格式转换和处理，请修改**mat_folder_path的文件夹路径**即可。

- **代码详解**

  **数据提取：**根据不同类型的数据的数据结构进行数据提取，以charge类型为例。

  ```python
  if cycle['type'][0] == 'charge':
      cycle_dict['Voltage_measured(V)'] = cycle_data['Voltage_measured'][0]
      cycle_dict['Current_measured(Amps)'] = cycle_data['Current_measured'][0]
      cycle_dict['Temperature_measured(degree C)'] = cycle_data['Temperature_measured'][0]
      cycle_dict['Current_charge(Amps)'] = cycle_data['Current_charge'][0]
      cycle_dict['Voltage_charge(V)'] = cycle_data['Voltage_charge'][0]
      cycle_dict['Time(s)'] = cycle_data['Time'][0]
  ```

  - 数据集中每个文件夹中的README.txt中都有对数据集5.+Battery+Data+Set数据结构的详细描述，如有需要请参考。



## Capacity.py

- **作用：**用于计算指定文件夹下的所有csv文件中的Capacity值

- **代码入口**

  在mat2csv.py中被调用

- **代码详解**

  **计算Capacity：**根据charge和discahrge类型的Time列和Current_measured(Amps)列进行计算，使用Current_measured(Amps)列作为用于积分的电流，类似的，如果需要使用到电压，一般也使用Voltage_measured(V)，这种带measured字样的。

  - **注意：**需要将时间单位统一为 h。

  ```python
  # 将时间单位转换为小时
  df['Time(hr)'] = df['Time(s)'] / 3600
  ```

  - **进行积分：**使用trapz函数根据每个时刻Time(h)对Current_measured(Amps)进行积分

  ```
  capacity = trapz(sub_cycle_group['Current_measured(Amps)'], sub_cycle_group['Time(hr)'])
  ```

  

  **异常值处理：**charge_Capacity和discharge_Capacity的数值分别对应正数和和负数，但在积分结果中容易出现异常值，需要做异常值处理

  - **charge类型的Capacity：**数值上 ≥ 0，异常数据(**小于零的数据**) = 0
  - **discharge类型的Capacity：**数值上 ≤ 0，异常数据(大于零的数据) = 0



## 文件夹A/B/C/D/E/F

A/B/C/D/E/F六个文件夹分别对应数据集5.+Battery+Data+Set中提供的六个文件夹1.XXX到6.XXX，使用时，只需要将数据集对应文件夹中的.mat文件复制到A/B/C/D/E/F文件夹中即可(**如，将1.XXX文件夹中的.mat文件复制到文件夹A中**)。

![image-20231112114449659](C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\image-20231112114449659.png)
