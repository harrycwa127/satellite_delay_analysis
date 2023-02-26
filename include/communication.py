from include import Satellite_class
from include import satcompute
from include import GroundStation_class
from include import visibility
from include import observation_class
from include.SimParameter_class import SimParameter
import sys


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

    transmit_delay = SimParameter.get_package_size() / SimParameter.get_data_rate()

    distance = satcompute.sat_ground_distance(t, sat, ground_station)

    propagation_delay = distance / SimParameter.get_signal_speed()        # radio speed near speed of light, 299,792,458 m per second, value in signal_speed is m/s

    total_delay  = transmit_delay + propagation_delay + SimParameter.get_buffer_delay() + SimParameter.get_process_delay()
    final_t = t + total_delay

    if visibility.is_gs_communicable(final_t, sat, ground_station):
        return final_t
    else:
        return -1

# input:    1. sat_list
#           2. gd
#           3. gs
#           4. offnadir

# output:   1. sat_commnicate_path
#           2. sat_commnicate_delay
def path_decision(sat_list: list, gd: observation_class.Observation, gs: GroundStation_class.GroundStation):

    t = 0

    imaging_sat = -1
    # search for all sat
    for s in range(len(sat_list)):
        if visibility.is_observation_visible(0, sat_list[s], gd):
            imaging_sat = s
            break

    # if no any satellite obervate the obervation point, exit
    if imaging_sat == -1:
        print("No Satellite able to visit the observation point!!")
        sys.exit(-1)


    # no able to directly transfer data from obervation satellite to ground station
    sat_commnicate_path = []
    sat_commnicate_path.append(imaging_sat)
    sat_commnicate_delay = []
    sat_commnicate_delay.append(0)
    sat_num = 0         #index of the last element in sat_commnicate_path and sat_commnicate_delay
    last_min_distance = -1

    end_path = False
    while end_path == False:
        ignore_sat = []
        ignore = True
        while ignore == True:
            min_distance = -1        # store the min distance from next satellite to gs
            min_sat = -1            # store the min distance satellite object index
            distance = -1

            for s in range(len(sat_list)):      # avoid the sat not able to communicate
                if s not in ignore_sat and s not in sat_commnicate_path:
                    if visibility.is_sat_communicable(t, sat_list[sat_commnicate_path[sat_num]], sat_list[s]):
                        distance = satcompute.sat_ground_distance(t, sat_list[s], gs)
                        if min_distance == -1:
                            min_distance = distance
                            min_sat = s
                        elif distance < min_distance:
                            min_distance = distance
                            min_sat = s

            # has sat in vibility
            if min_sat != -1:
                temp = inter_sat_commnicate(t, sat_list[sat_commnicate_path[sat_num]], sat_list[min_sat])
                if temp > 0:
                    # commnicate success
                    t = temp
                    sat_commnicate_path.append(min_sat)
                    sat_num += 1
                    ignore = False

                    # insert delay
                    sat_commnicate_delay.append(t)

                    if visibility.is_gs_communicable(t, sat_list[sat_commnicate_path[sat_num]], gs) == True:
                        temp = sat_ground_commnicate(t, sat_list[sat_commnicate_path[sat_num]], gs)
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
                    sat_commnicate_path.append(-1)  # mean waiting
                    sat_commnicate_delay.append(t)
                    print("No other Satellites in the visibility, wait 1 sec.")

    return (sat_commnicate_path, sat_commnicate_delay)
