import os
import xlwt
import time
import numpy as np
import math
# import backup.include.imaging as imaging
import include.communication as communication
import include.greenwich as greenwich
import include.satclass as satclass
# import backup.include.gdclass as gdclass
import include.gsclass as gsclass

start_time = time.time()
requestNum = 144

# ---------read start time and end time
time_f = open('settings/TIME_INTERVAL.txt', 'r')
time_lines = []
for line in time_f.readlines():
    time_lines.append(line.split())
start_time_julian = greenwich.julian2(int(time_lines[0][0]), int(time_lines[0][1]), int(time_lines[0][2]),
                                      int(time_lines[0][3]), int(time_lines[0][4]), int(time_lines[0][5]))
end_time_julian = greenwich.julian2(int(time_lines[1][0]), int(time_lines[1][1]), int(time_lines[1][2]),
                                    int(time_lines[1][3]), int(time_lines[1][4]), int(time_lines[1][5]))
time_interval = (end_time_julian-start_time_julian)*86400  # 单位s
start_greenwich = (greenwich.greenwich(start_time_julian)) % 360   # 转到0到360°

# ---------read ground stations
gs_lines = []
input_f2 = open('settings/SELECT_GROUND_STATION2.txt', 'r')
for line in input_f2.readlines():
    tmpl = line.strip()
    gs_lines.append(tmpl.split(' '))
input_f2.close()
gs_accounts = len(gs_lines)
gs_list = []
for g in range(gs_accounts):
    gs_lat = float(gs_lines[g][0])
    gs_long = float(gs_lines[g][1])
    if gs_long < 0:
        gs_long = 360 + gs_long
    gs_ele = float(gs_lines[g][2])
    # gs_ele = 10
    gs_lat_rad = math.radians(gs_lat)  # 弧度
    gs_long_rad = math.radians(gs_long)  # 弧度
    gs_ele_rad = math.radians(gs_ele)  # 弧度
    gs = gsclass.GS(gs_lat_rad, gs_long_rad, gs_ele_rad)
    gs_list.append(gs)

# ----------main section
off_nadir = math.radians(45)
i_o = math.radians(97)
e_o = 0
omega_o = 0
circle_o = 14
m = 9                  # number of orbit
n = 25                 # number of sat

request_period = 600   # request period (s)
request_postpone = 60  # request postpone (s)

img_cost = 1           # imaging cost (s)
com_cost = 15          # communication cost (s)
ser_ddl = 150          # service delay (s)

# 删除output文件
if os.path.exists("results/baseline_result.xls"):
    os.remove("results/baseline_result.xls")
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('baseline_result', cell_overwrite_ok=True)
col = ('satellite id', 'orbit id', 'communicatable with ground station')
for i in range(0, 3):
    sheet.write(0, i, col[i])
col_num = 1

# ------初始化所有卫星
sat_list = []
first_Omega = 0  # 第一个轨道的升交点赤经
even_Omega = 180 / (m-1)
for orbit_id in range(m):
    Omega_o = math.radians(first_Omega + orbit_id * even_Omega)
    first_M = 0  # 轨道上的第一个卫星的位置
    even_M = 360 / n
    for sat_id in range(n):
        M_o = math.radians(first_M + sat_id * even_M)
        # 令卫星的当前时间为simulation的开始时间
        s = satclass.Sat(start_time_julian, i_o, Omega_o, e_o, omega_o, M_o, circle_o, start_time_julian, orbit_id, sat_id)
        
        sat_list = sat_list + [s]

# 看能否通信
target_gs = gs_list[0]
for s in sat_list:
    sheet.write(col_num, 0, s.sat_id)
    sheet.write(col_num, 1, s.orbit_id)
    gs_off_nadir = math.asin(satclass.Re * math.cos(target_gs.ele_rad) / s.r)
    if communication.is_communicable(0, s, gs, gs_off_nadir, start_greenwich):
        print("satellite", s.sat_id,"in orbit", s.orbit_id, "can communication with target ground satation")
        sheet.write(col_num, 2, "True")
    else:
        sheet.write(col_num, 2, "False")

    col_num+=1

end_time = time.time()
print('overall time:',  end_time-start_time)
book.save('results/baseline_result.xls')


#     sheet.write(col_num, 0, math.degrees(gd_list[i].lat_rad))
    # sheet.write(col_num, 1, math.degrees(gd_list[i].long_rad))