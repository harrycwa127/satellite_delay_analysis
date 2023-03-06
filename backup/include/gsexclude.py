from backup import gdclass
from include import GroundStation_class
import math


def exclude_ground_station(gd: gdclass.Observation, gs: GroundStation_class.GroundStation, max_rad):
    delta_phi = gd.lat_rad-gs.lat_rad
    delta_lam = gd.lon_rad-gs.lon_rad
    temp1 = math.sin(delta_phi/2)**2
    temp2 = math.cos(gd.lat_rad)*math.cos(gs.lat_rad)*math.sin(delta_lam/2)*math.sin(delta_lam/2)
    delta = 2*math.asin(math.sqrt(temp1+temp2))
    if delta > max_rad:
        return True
    return False
