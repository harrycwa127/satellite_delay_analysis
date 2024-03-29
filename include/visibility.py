from include import Satellite_class
from include import GroundStation_class
from include import satcompute
from include import Observation_class
from include.Setting_class import Setting
import math


# Determine whether the satellite can image the obervation point
# input：1.t
#       2.sat
#       3.obervation point
# output：TRUE OR FALSE
def is_observation_visible(t, satellite: Satellite_class.Satellite, gd: Observation_class.Observation) -> bool:
    phi, lam = satcompute.get_sat_lat_lon(sat = satellite, t = t)

    theta = lam - gd.lon_rad
    cos_psi = math.cos(gd.lat_rad) * math.cos(phi) * math.cos(theta) + math.sin(gd.lat_rad) * math.sin(phi)
    psi = math.acos(cos_psi)
    beta = math.atan(Satellite_class.Re * math.sin(psi) / (satellite.r - Satellite_class.Re * math.cos(psi)))  # off nadir angle, 注意atan得到的是[-pi/2,pi/2]
    if cos_psi > Satellite_class.Re / satellite.r and beta <= Setting.off_nadir:
        return True
    else:
        return False


# Determine whether the satellite can communicate with ground station
# input：1.t
#      2.sat
#      3.gs
# output：TRUE OR FALSE
def is_gs_communicable(t, satellite: Satellite_class.Satellite, gs: GroundStation_class.GroundStation) -> bool:
    gs_off_nadir = math.asin(Satellite_class.Re * math.cos(gs.ele_rad) / satellite.r)
    phi, lam = satcompute.get_sat_lat_lon(sat = satellite, t = t)
    
    theta = lam - gs.lon_rad
    cos_psi = math.cos(gs.lat_rad) * math.cos(phi) * math.cos(theta) + math.sin(gs.lat_rad) * math.sin(phi)
    psi = math.acos(cos_psi)
    beta = math.atan(Satellite_class.Re * math.sin(psi) / (satellite.r - Satellite_class.Re * math.cos(psi)))  # off nadir angle, 注意atan得到的是[-pi/2,pi/2]

    if cos_psi > (Satellite_class.Re / satellite.r) and beta <= gs_off_nadir:
        return True
    else:
        return False

# Determine whether the satellite can communicate with another sat
# input：1.t
#      2.sat1
#      3.sat2
# output：TRUE OR FALSE
def is_sat_communicable(t, from_satellite: Satellite_class.Satellite, to_satellite: Satellite_class.Satellite) -> bool:
    r3 = satcompute.inter_sat_distance(t, from_satellite, to_satellite)

    beta = math.acos((r3**2 + from_satellite.r**2 - to_satellite.r**2) / (2 * r3 * from_satellite.r))

    off_nadir_limit = math.asin(Satellite_class.Re/from_satellite.r)

    if beta > off_nadir_limit:
        return True
    else:
        return False
