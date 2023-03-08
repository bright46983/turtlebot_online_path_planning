import numpy as np
import math
from ompl import base as ob
from ompl import geometric as og

def wrap_angle(angle):
    return (angle + ( 2.0 * np.pi * np.floor( ( np.pi - angle ) / ( 2.0 * np.pi ) ) ) )

class StateValidityChecker:
    """ Checks if a position or a path is valid given an occupancy map."""

    # Constructor
    def __init__(self, distance=0.1, is_unknown_valid=True):
        # map: 2D array of integers which categorizes world occupancy
        self.map = None 
        # map sampling resolution (size of a cell))                            
        self.resolution = None
        # world position of cell (0, 0) in self.map                      
        self.origin = None
        # set method has been called                          
        self.there_is_map = False
        # radius arround the robot used to check occupancy of a given position                 
        self.distance = distance                    
        # if True, unknown space is considered valid
        self.is_unknown_valid = is_unknown_valid    
    
    # Set occupancy map, its resolution and origin. 
    def set(self, data, resolution, origin):
        self.map = data
        self.resolution = resolution
        self.origin = np.array(origin)
        self.there_is_map = True
    
    # Given a pose, returs true if the pose is not in collision and false othewise.
    def is_valid(self, pose): 

        # TODO: convert world robot position to map coordinates using method __position_to_map__
        # TODO: check occupancy of the vicinity of a robot position (indicated by self.distance atribute). 
        # Return True if free, False if occupied and self.is_unknown_valid if unknown. 
        # If checked position is outside the map bounds consider it as unknown.
        ...

    # Given a path, returs true if the path is not in collision and false othewise.
    def check_path(self, path):

        # TODO: Discretize the positions between 2 waypoints with an step_size = 2*self.distance
        # TODO: for each point check if `is_valid``. If only one element is not valid return False, otherwise True. 

    # Transform position with respect the map origin to cell coordinates
    def __position_to_map__(self, p):

        # TODO: convert world position to map coordinates. 
        ...
    

# Planner: This function has to plan a path from start_p to goal_p. To check if a position is valid the 
# StateValidityChecker class has to be used. The planning dominion must be specified as well as the maximum planning time.
# The planner returns a path that is a list of poses ([x, y]).
def compute_path(start_p, goal_p, state_validity_checker, bounds, max_time=1.0):

    # TODO: Plan a path from start_p to goal_p inside bounds using the OMPL and the state_validity_checker object. Follow notebook example.
    # some code
    # TODO: if solved, return a list with the [x, y] points in the solution path
    # TODO: Ensure that the path brings the robot to the goal (with a small tolerance)!

    return ...


# Controller: Given the current position and the goal position, this function computes the desired 
# lineal velocity and angular velocity to be applied in order to reah the goal.
def move_to_point(current, goal, Kv=0.5, Kw=0.5):
    
    # TODO: Implement a proportional controller which sets a velocity command to move from current position to goal (u = Ke)
    # Make it sequential to avoid strange curves. First correct orientation and then distance. 
    # Hint: use wrap_angle function to maintain yaw in [-pi, pi]
    # This function should return only  linear velocity (v) and angular velocity (w)
    
    return v, w
