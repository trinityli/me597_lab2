# Imports


import sys

from utilities import euler_from_quaternion, calculate_angular_error, calculate_linear_error
from pid import PID_ctrl

from rclpy import init, spin, spin_once
from rclpy.node import Node
from geometry_msgs.msg import Twist

from rclpy.qos import QoSProfile
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from nav_msgs.msg import Odometry as odom

from localization import localization, rawSensor

from planner import TRAJECTORY_PLANNER, POINT_PLANNER, planner
from controller import controller, trajectoryController
import rclpy

# You may add any other imports you may need/want to use below
# import ...
import rclpy 
import argparse


class decision_maker(Node):
    
    def __init__(self, publisher_msg, publishing_topic, qos_publisher, goalPoint, rate=10, motion_type=POINT_PLANNER):

        super().__init__("decision_maker")

        #TODO Part 4: Create a publisher for the topic responsible for robot's motion
        self.publisher = self.create_publisher(Twist, publishing_topic, qos_publisher)        

        publishing_period=1/rate
        
        # Instantiate the controller
        # TODO Part 5: Tune your parameters here
    
        if motion_type == POINT_PLANNER:
            #self.controller=controller(klp=0.05, klv=0.0, kap=0.8, kav=0.0)      
            self.controller=controller(klp=0.05, klv=0.0, kap=0.8, kav=0.0)      
            self.planner=planner(POINT_PLANNER)    
    
    
        elif motion_type==TRAJECTORY_PLANNER:
            #self.controller=trajectoryController(klp=0.1, klv=0.2, kap=0.05, kav=0.2) #Simulation tune
            #self.controller=trajectoryController(klp=0.5, klv=0.5, kap=0.8, kav=0.6) #Lab PID settings
            self.controller=trajectoryController(klp=0.5, klv=0, kli=0, kap=0.8, kav=0, kai=0) #P Controller
            self.planner=planner(TRAJECTORY_PLANNER)

        else:
            print("Error! you don't have this planner", file=sys.stderr)


        # Instantiate the localization, use rawSensor for now  
        self.localizer=localization(rawSensor)

        # Instantiate the planner
        # NOTE: goalPoint is used only for the pointPlanner
        self.goal=self.planner.plan(goalPoint)

        self.create_timer(publishing_period, self.timerCallback)


    def timerCallback(self):
 
        # TODO Part 3: Run the localization node
        rclpy.spin_once(self.localizer)

        if self.localizer.getPose()  is  None:
            print("waiting for odom msgs ....")
            return

        vel_msg=Twist()

        print(self.localizer.getPose())
        current_pose = self.localizer.getPose()
        
        # TODO Part 3: Check if you reached the goal
        position_threshold = 0.1
        if type(self.goal) == list:
            last_goal_point = self.goal[-1]
            goal_x, goal_y = last_goal_point[0], last_goal_point[1]
            reached_goal = (abs(current_pose[0] - goal_x) < position_threshold and abs(current_pose[1] - goal_y) < position_threshold)
        else: 
            goal_x, goal_y, goal_theta = self.goal
            reached_position = (abs(current_pose[0] - goal_x) < position_threshold and
                                abs(current_pose[1] - goal_y) < position_threshold)
            orientation_threshold = 0.1  # radians
            reached_orientation = abs(current_pose[2] - goal_theta) < orientation_threshold
            reached_goal = reached_position and reached_orientation        

        if reached_goal:
            print("reached goal")
            self.publisher.publish(vel_msg)
            
            self.controller.PID_angular.logger.save_log()
            self.controller.PID_linear.logger.save_log()
            
            #TODO Part 3: exit the spin
            rclpy.shutdown() 
        
        velocity, yaw_rate = self.controller.vel_request(self.localizer.getPose(), self.goal, True)
        print("Velocity and yaw", velocity, yaw_rate)
        #TODO Part 4: Publish the velocity to move the robot
        vel_msg.linear.x = float(velocity)
        vel_msg.angular.z = float(yaw_rate)

        self.publisher.publish(vel_msg) 

def main(args=None):
    
    init()
    # TODO Part 3: You migh need to change the QoS profile based on whether you're using the real robot or in simulation.
    # Remember to define your QoS profile based on the information available in "ros2 topic info /odom --verbose" as explained in Tutorial 3
    
    odom_qos=QoSProfile(reliability=2, durability=2, history=1, depth=10)
    cmd_vel_qos = QoSProfile(history=QoSHistoryPolicy.KEEP_LAST,
                        depth=10,
                        #reliability=QoSReliabilityPolicy.BEST_EFFORT,
                        durability=QoSDurabilityPolicy.VOLATILE)
        
    # TODO Part 3: instantiate the decision_maker with the proper parameters for moving the robot
    goal = [0.0, 0.0, 0.0]
    publishing_topic = 'cmd_vel'

    #localizer = localization()
    
    if args.motion.lower() == "point":
        DM = decision_maker(publisher_msg=Twist(), publishing_topic=publishing_topic, qos_publisher=cmd_vel_qos, goalPoint=goal, motion_type=POINT_PLANNER)    
    elif args.motion.lower() == "trajectory":
        DM = decision_maker(publisher_msg=Twist(), publishing_topic=publishing_topic, qos_publisher=cmd_vel_qos, goalPoint=goal, motion_type=TRAJECTORY_PLANNER) 
    else:
        print("invalid motion type", file=sys.stderr)        
    
    try:
        spin(DM)
    except SystemExit:
        print(f"reached there successfully {DM.localizer.pose}")


if __name__=="__main__":

    argParser=argparse.ArgumentParser(description="point or trajectory") 
    argParser.add_argument("--motion", type=str, default="point")
    args = argParser.parse_args()
    main(args)