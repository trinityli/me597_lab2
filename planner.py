import math

# Type of planner
POINT_PLANNER=0; TRAJECTORY_PLANNER=1



class planner:
    def __init__(self, type_):

        self.type=type_

    
    def plan(self, goalPoint=[-1.0, -1.0, 0.0]):
        
        if self.type==POINT_PLANNER:
            return self.point_planner(goalPoint)
        
        elif self.type==TRAJECTORY_PLANNER:
            return self.trajectory_planner()


    def point_planner(self, goalPoint):
        x = goalPoint[0]
        y = goalPoint[1]
        theta = goalPoint[2]
        return x, y, theta

    # TODO Part 6: Implement the trajectories here
    def trajectory_planner(self):
        x_goal = 2
        x_start = 0 #-x_goal  #
        x_end = x_goal  

        trajectory = []
        num_points = 40
        for i in range(num_points + 1):  
            #x = x_start + i * ((x_end - x_start) / num_points)
            #y = 1 / (1 + math.exp(-x))  # Sigmoid function
            x = i * (x_goal / num_points)
            y = x ** 2  # Calculate y based on the new trajectory formula y = x^2
            trajectory.append([x, y])
        print("Trajectory: ", trajectory)
        return trajectory
        

    # def trajectory_planner_sigmoid(self, goalPoint):
    #     x_goal, _, _ = goalPoint  
    #     trajectory = []
    #     num_points = 10
    #     x_start = -x_goal  #
    #     x_end = x_goal  
        
    #     for i in range(num_points + 1):
    #         # Linearly space x values from x_start to x_end
    #         x = x_start + i * ((x_end - x_start) / num_points)
    #         y = 1 / (1 + math.exp(-x))  # Sigmoid function
    #         trajectory.append([x, y])
    #     return trajectory