import math
from include import Satellite_class
from include import satcompute
from include import GroundStation_class
from include import visibility
from include import observation_class
from include.SimParameter_class import SimParameter
import sys


# simulate一段时间内，卫星和地面站通信的时间段
# 输入：1.要simulate的时间段（从开始时刻0算起）
#      2.开始时刻0经度所处的赤经
#      3.卫星class
#      4.地面站class
# 输出：communication curve
# def communicable(time_interval, satellite: Satellite_class.Satellite, gs: GroundStation_class.GroundStation):
#     # 根据仰角范围求off nadir角最大值
#     gs_off_nadir = math.asin(Satellite_class.Re * math.cos(gs.ele_rad) / satellite.r)
#     start_ground = (math.radians(SimParameter.get_start_greenwich()) + gs.long_rad) % (2 * math.pi)
#     psi, phi_min, phi_max = satcompute.get_sat_phi_range(gs_off_nadir, satellite.r, gs.lat_rad)
#     alpha_min1, alpha_max1, alpha_min2, alpha_max2, t_min1, t_max1, t_min2, t_max2 = satcompute.get_sat_alpha_range\
#         (phi_min, phi_max, satellite)
#     all_seen, gd_rang_of_alpha1, gd_rang_of_alpha2 = satcompute.get_observation_alpha_range\
#         (psi, phi_min, phi_max, satellite.i_o, alpha_min1, alpha_max1, alpha_min2, alpha_max2)

#     vs = []
#     nvs = []
#     num = math.ceil(time_interval / satellite.T_o)
#     test = 0
#     for n in range(num + 1):
#         t1 = min(max(int(t_min1 + n * satellite.T_o), 0), time_interval)
#         t2 = min(max(t_max1 + n * satellite.T_o, 0), time_interval)
#         ground_alpha_min = (start_ground + Satellite_class.omega_e * t1) % (2 * math.pi)
#         ground_alpha_max = (start_ground + Satellite_class.omega_e * t2) % (2 * math.pi)
#         abandon = 0
#         if all_seen == 1:
#             abandon = 0
#         elif gd_rang_of_alpha1[0] <= gd_rang_of_alpha1[1]:
#             if ground_alpha_min < gd_rang_of_alpha1[0] and ground_alpha_max < gd_rang_of_alpha1[0]:
#                 abandon = 1
#             if ground_alpha_min > gd_rang_of_alpha1[1] and ground_alpha_max > gd_rang_of_alpha1[1]:
#                 abandon = 1
#         else:
#             if gd_rang_of_alpha1[1] < ground_alpha_min < gd_rang_of_alpha1[0] \
#                     and gd_rang_of_alpha1[1] < ground_alpha_max < gd_rang_of_alpha1[0] \
#                     and ground_alpha_min <= ground_alpha_max:
#                 abandon = 1
#         if t1 == t2:
#             abandon = 1
#         if abandon == 0:
#             t = t1
#             while t < t2+1:
#                 if visibility.is_gs_communicable(t, satellite, gs, gs_off_nadir, start_greenwich):
#                     if test == 0:
#                         #print('t1:', t)
#                         test = 1
#                         vs.append(round(t, 1))
#                 else:
#                     if test:
#                         #print('t2:', t)
#                         test = 0
#                         nvs.append(round(t, 1))
#                 t = t + 0.1

#         t3 = min(max(int(t_min2 + n * satellite.T_o), 0), time_interval)
#         t4 = min(max(t_max2 + n * satellite.T_o, 0), time_interval)
#         ground_alpha_min = (start_ground + Satellite_class.omega_e * t3) % (2 * math.pi)
#         ground_alpha_max = (start_ground + Satellite_class.omega_e * t4) % (2 * math.pi)
#         abandon = 0
#         if all_seen == 1:
#             abandon = 0
#         elif gd_rang_of_alpha2[0] <= gd_rang_of_alpha2[1]:
#             if ground_alpha_min < gd_rang_of_alpha2[0] and ground_alpha_max < gd_rang_of_alpha2[0]:
#                 abandon = 1
#             if ground_alpha_min > gd_rang_of_alpha2[1] and ground_alpha_max > gd_rang_of_alpha2[1]:
#                 abandon = 1
#         else:
#             if gd_rang_of_alpha2[1] < ground_alpha_min < gd_rang_of_alpha2[0] \
#                     and gd_rang_of_alpha2[1] < ground_alpha_max < gd_rang_of_alpha2[0] \
#                     and ground_alpha_min <= ground_alpha_max:
#                 abandon = 1
#         if t3 == t4:
#             abandon = 1
#         if abandon == 0:
#             t = t3
#             while t < t4+1:
#                 if visibility.is_gs_communicable(t, satellite, gs, gs_off_nadir, start_greenwich):
#                     if test == 0:
#                         #print('t3:', t)
#                         test = 1
#                         vs.append(round(t, 1))
#                 else:
#                     if test:
#                         #print('t4:', t)
#                         test = 0
#                         nvs.append(round(t, 1))
#                 t = t + 0.1
#     #print('vs:', vs)
#     #print('nvs:', nvs)
#     if test:
#         nvs.append(round(time_interval))
#     curve = []
#     interval = []
#     sum_t = 0
#     if len(vs) == len(nvs):
#         for v in range(len(vs)):
#             curve.append([vs[v], nvs[v]])
#             interval.append(nvs[v] - vs[v])
#             sum_t = sum_t + (nvs[v] - vs[v])
#     else:
#         print(satellite)
#         print(gs)
#         print('off nadir:', gs_off_nadir)
#         print('vs:', vs)
#         print('nvs:', nvs)
#         print("error type: vs is not equal to nvs")
#         exit()
#     return curve

# asuum satellite using radio frequencies, because only very less satellite use laser
# high carrier frequencies and narrow beamwidths
# The signal delay approximately 20 ms.

# input:    1. t (time passed from start_time_julian)
#           2. package_size(size of data)
#           3. signal_speed(speed of signal)
#           4. from_sat (the satellite hold the data)
#           5. to_sat (the satellite transfer the data)
#           6. buffer_delay (the sum of the delays that occur at each hop in the network due to cell queuing)
#           7. process_delay (the on-board switching and processing delay from satellite)

# output:   t (the time passed from start_time_julian after commnicate), 
#           when > 0 commnicate success, < 0 fail

# reference https://www.researchgate.net/publication/1961144_Analysis_and_Simulation_of_Delay_and_Buffer_Requirements_of_satellite-ATM_Networks_for_TCPIP_Traffic

def inter_sat_commnicate(t, from_sat: Satellite_class.Satellite, to_sat: Satellite_class.Satellite) -> float:
    transmit_delay = SimParameter.get_package_size() / SimParameter.get_data_rate()

    inter_sat_distance = satcompute.inter_sat_distance(t, from_sat, to_sat)

    propagation_delay = inter_sat_distance / SimParameter.get_signal_speed()   # radio speed near speed of light, 299,792,458 m per second, value in signal_speed is m/s

    total_delay = transmit_delay + propagation_delay + SimParameter.get_buffer_delay() + SimParameter.get_process_delay()
    final_t = t + total_delay

    if visibility.is_sat_communicable(final_t, from_sat, to_sat):
        return final_t
    else:
        return -1


# input:    1. t (time passed from start_greenwich, in sec)
#           2. package_size(size of data)
#           3. data_rate (data rate of transmission)
#           4. 
#           5. from_sat (the satellite hold the data)
#           6. to_sat (the satellite transfer the data)
#           7. buffer_delay (the delays that occur at each hop in the network due to cell queuing)
#           8. process_delay (the on-board switching and processing delay from satellite)

# output:   t (the time passed from start_time_julian after commnicate), 
#           when > 0 commnicate success, < 0 fail

def sat_ground_commnicate(t, sat: Satellite_class.Satellite, ground_station: GroundStation_class.GroundStation) -> float:
    gs_off_nadir = math.asin(Satellite_class.Re * math.cos(ground_station.ele_rad) / sat.r)

    transmit_delay = SimParameter.get_package_size() / SimParameter.get_data_rate()

    distance = satcompute.sat_ground_distance(sat, ground_station)

    propagation_delay = distance / SimParameter.get_signal_speed()        # radio speed near speed of light, 299,792,458 m per second, value in signal_speed is m/s

    total_delay  = transmit_delay + propagation_delay + SimParameter.get_buffer_delay() + SimParameter.get_process_delay()
    final_t = t + total_delay

    if visibility.is_gs_communicable(final_t, sat, ground_station, gs_off_nadir, SimParameter.get_start_greenwich()):
        return final_t
    else:
        return -1

# input:    1. sat_list
#           2. gd
#           3. gs
#           4. offnadir

# output:   1. sat_commnicate_path
#           2. sat_commnicate_delay
def path_decision(sat_list: list(Satellite_class.Satellite), gd: observation_class.Observation, gs: GroundStation_class.GroundStation) -> tuple(list, list(float)):

    t = 0

    imaging_sat = -1
    # search for all sat
    for s in range(len(sat_list)):
        if visibility.is_observation_visible(0, sat_list[s], gd, SimParameter.get_off_nadir()):
            imaging_sat = s
            break

    # if no any satellite obervate the obervation point, exit
    if imaging_sat == -1:
        print("No Satellite able to visit the observation point!!")
        sys.exit(-1)


    # no able to directly transfer data from obervation satellite to ground station
    sat_commnicate_path = []
    sat_commnicate_path.append(imaging_sat)
    sat_num = 0         #index of the last element in sat_commnicate_path
    sat_commnicate_delay = []
    sat_commnicate_delay.append(0)

    end_path = False
    while end_path == False:
        ignore_sat = []
        ignore = True
        while ignore == True:
            min_distance = -1        # store the min distance from next satellite to gs
            min_sat = -1            # store the min distance satellite object
            distance = 0

            for s in range(len(sat_list)):      # avoid the sat not able to communicate
                if s not in ignore_sat and s not in sat_commnicate_path:
                    if visibility.is_sat_communicable(sat_list[sat_commnicate_path[sat_num]], sat_list[s]):
                        distance = satcompute.sat_ground_distance(sat_list[s], gs)
                        if min_distance == -1:
                            min_distance = distance
                            min_sat = s
                        elif distance < min_distance:
                            min_distance = distance
                            min_sat = s

            # has sat in vibility
            if min_sat != -1:
                temp = inter_sat_commnicate(sat_list[sat_commnicate_path[sat_num]], sat_list[min_sat])
                if temp > 0:
                    # commnicate success
                    t = temp
                    sat_commnicate_path.append(min_sat)
                    sat_num += 1
                    ignore = False

                    # insert delay
                    sat_commnicate_delay.append(t)

                    if visibility.is_gs_communicable(sat_list[sat_commnicate_path[sat_num]], gs) == True:
                        temp = sat_ground_commnicate(sat_list[sat_commnicate_path[sat_num]], gs)
                        if temp > 0:
                            t = temp
                            end_path = True
                        else:
                            end_path = False

                else:
                    # commnication fail, loop again and ignore that sat
                    ignore = True
                    ignore_sat.append(min_sat)
                    
            # wait 1 sec and check visibility again
            else:
                    t += 1
                    print("No other Satellites in the visibility, wait 1 sec.")

    return (sat_commnicate_path, sat_commnicate_delay)
