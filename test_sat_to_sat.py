import os
import xlwt
import time
import math
from include import Satellite_class
from include import satcompute
from include import visibility
from include import read_data
from include.Setting_class import Setting


start_time = time.time()

# ---------read start time and end time



# remove orginal output file
if os.path.exists("results/sat_to_sat_communicable_result.xls"):
    os.remove("results/sat_to_sat_communicable_result.xls")
book = xlwt.Workbook(encoding='utf-8', style_compression=0)
sheet = book.add_sheet('sat_to_sat_communicable_result', cell_overwrite_ok=True)
col = ('Geocentric Latitude', 'Geocentric Longitude', 'Radius of Orbit', 'communicable')
for i in range(0, 4):
    sheet.write(0, i, col[i])
col_num = 1

# init satellites
off_nadir = math.radians(45)
i_o = math.radians(97)
omega_o = 0
circle_o = 14
n = 200       # number of sat

sat_list = []
first_Omega = 0  # longitude of ascending node of the first orbit
Omega_o = math.radians(first_Omega)
first_M = 0  # first satellite position in this orbit
even_M = 360 / n
for sat_id in range(n):
    M_o = math.radians(first_M + sat_id * even_M)
    # set current time to start time
    s = Satellite_class.Satellite(Omega_o, M_o, Setting.start_time_julian)
    
    sat_list = sat_list + [s]

# 看能否通信
target_sat = Satellite_class.Satellite(Setting.start_time_julian, i_o, Omega_o, omega_o, first_M, 10, Setting.start_time_julian)
phi, lam = satcompute.get_sat_lat_lon(sat = target_sat, t = 0)
for s in sat_list:
    # find out the lat lon
    phi, lam = satcompute.get_sat_lat_lon(sat = s, t = 0)

    # write data to xls
    sheet.write(col_num, 0, phi)
    sheet.write(col_num, 1, lam)
    sheet.write(col_num, 2, s.r)

    # check communicable and write result to xls
    if visibility.is_sat_communicable(0, target_sat, s):
        # print("satellite", s.sat_id,"in orbit", s.orbit_id, "can communication with the target satellite")
        sheet.write(col_num, 3, "True")
    else:
        sheet.write(col_num, 3, "False")

    col_num+=1

end_time = time.time()
print('overall time:',  end_time-start_time)
book.save('results/sat_to_sat_communicable_result.xls')