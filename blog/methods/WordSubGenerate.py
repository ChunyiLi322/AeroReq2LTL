import csv

# 给定文本
text = """
tmpPSBIT        加电状态 1加电 0断电
tmpHTBIT        健康状态 0健康 1不健康
StateFlag       可用标志 TRUE可用 FALSE不可用
wa			    陀螺角速度模拟量
wa_out          剔野后的陀螺角速度模拟量
wal				上周期陀螺角速度模拟量
countPick		剔野计数器
waThr           剔野限
pickThr         连续阈值
StateFlag       陀螺可用标志
JoinTotal       参加定姿的陀螺个数 
gyroStatus0		陀螺状态 
SignFlag    	参加定姿的陀螺序号
royaw           太敏滚动角 
piyaw           太敏俯仰角 
flgSp           见太阳标志 
ADDR_AD_START   AD采集启动地址 0xA000 
AD_SS_LO4       AD采集数据低4位地址 0xA003 
AD_SS_HI8       AD采集数据高8位地址 0xA001 
SP_ADDR         见太阳标志地址 0xE000 
SP_BIT          见太阳标志位  
chnl            AD采集通道号 
JoinTotal       参加定姿的陀螺个数
gyroStatus0     陀螺状态旧
SignFlag		参加定姿的陀螺序号数组指针 
flgGryoCalc     陀螺计算标志 
Rtemp    	 	矩阵计算结果 
gyroStatus1		陀螺状态新 
SAM_DAMP        速率阻尼
SAM_PITCH       俯仰搜索  
SAM_ROLL        滚动搜索  
SAM_CRUISE      巡航  
NOCTRL          不控
pRate           三轴姿态角速度
pAngle          三轴姿态角度
u               输出的三轴控制量
CTRL_PARAM_SAM  控制器系数
destRate        三轴角速度偏置
mController     控制器内部数据结构
Yp              脉冲方向输出数组指针（正方向）
Yn              脉冲方向输出数组指针（负方向）
wPulse          推力器组合后的输出值
pu              三轴控制器输出量
Yp              各轴是否正向喷气    ip03的，和ip02变量名重复，但含义不同
Yn              各轴是否负向喷气    ip03的，和ip02变量名重复
h1              开坎值
r               反馈信号
pGyroRate       陀螺三轴角速度
workMode        当前太阳搜索子模式
m_countMode     子模式内部计时器
m_countPublic   子模式共用计时器
time_D2P        速率阻尼连续稳定转俯仰搜索时间
time_D2P_overtime 速率阻尼不能稳定转俯仰搜索时间
Gi              陀螺角度
W               陀螺三轴角速度
"""

# 将文本划分成两列数据
lines = text.strip().split('\n')
data = [[line[:15].strip(), line[15:].strip()] for line in lines]

# 写入CSV文件
with open('variables.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Variable Name', 'Variable Description'])
    for row in data:
        writer.writerow(row)

print("CSV 文件已生成")
