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
import include.satcompute as satcompute

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
time_interval = (end_time_julian-start_time_julian)*86400  # in sec
start_greenwich = (greenwich.greenwich(start_time_julian)) % 360   # from 0 to 360 degree
# ----------main section
off_nadir = math.radians(45)
i_o = math.radians(97)
e_o = 0
omega_o = 0
circle_o = 14
n = 200                 # number of sat


# 删除output文件
if os.path.exists("results/sat_to_sat_communicable_result.xls"):
    os.remove("results/sat_to_sat_communicable_result.xls")
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('sat_to_sat_communicable_result', cell_overwrite_ok=True)
col = ('satellite id', 'orbit id', 'Geocentric Latitude', 'Geocentric Longitude', 'communicable')
for i in range(0, 5):
    sheet.write(0, i, col[i])
col_num = 1

# init satellites
sat_list = []
first_Omega = 0  # longitude of ascending node of the first orbit
Omega_o = math.radians(first_Omega)
first_M = 0  # first satellite position in this orbit
even_M = 360 / n
for sat_id in range(n):
    M_o = math.radians(first_M + sat_id * even_M)
    # set current time to start time
    s = satclass.Sat(start_time_julian, i_o, Omega_o, e_o, omega_o, M_o, circle_o, start_time_julian, 0, sat_id)
    
    sat_list = sat_list + [s]

# 看能否通信
target_sat = satclass.Sat(start_time_julian, i_o, Omega_o, e_o, omega_o, first_M, 15, start_time_julian, 0, -1)
phi, lam = satcompute.get_sat_geo_lat_lon(sat = target_sat, t = 0, start_greenwich = start_greenwich)
print(phi, lam, target_sat.r)
for s in sat_list:
    # find out the lat lon
    phi, lam = satcompute.get_sat_geo_lat_lon(sat = s, t = 0, start_greenwich = start_greenwich)

    # write data to xls
    sheet.write(col_num, 0, s.sat_id)
    sheet.write(col_num, 1, s.orbit_id)
    sheet.write(col_num, 2, phi)
    sheet.write(col_num, 3, lam)
    sheet.write(col_num, 4, s.r)

    # check communicable and write result to xls
    # gs_off_nadir = math.asin(satclass.Re * math.cos(target_gs.ele_rad) / s.r)
    if communication.is_sat_communicable(0, target_sat, s, start_greenwich):
        print("satellite", s.sat_id,"in orbit", s.orbit_id, "can communication with the target satellite")
        sheet.write(col_num, 5, "True")
    else:
        sheet.write(col_num, 5, "False")

    col_num+=1

end_time = time.time()
print('overall time:',  end_time-start_time)
book.save('results/sat_to_sat_communicable_result.xls')