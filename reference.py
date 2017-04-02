"""A module that contains useful default values that can be used to quickly initialize simulations"""

import scripts


def d_plant_scripts():
    """Default plant scripts"""
    return [[scripts.StayStill()], [scripts.StayStill()], [scripts.StayStill()]]


def d_versatile_scripts():
    """default versatile scripts"""
    return[[scripts.HuntWeaker()], [scripts.HuntWeaker()], [scripts.StayStill()]]
