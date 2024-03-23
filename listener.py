import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import csv
from utilities import euler_from_quaternion

from rclpy.qos import QoSProfile
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from nav_msgs.msg import Odometry as odom
from rclpy.time import Time

odom_qos=QoSProfile(reliability=2, durability=2, history=1, depth=10)


class OdomSubscriber(Node):
    def __init__(self):
        super().__init__('odom_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.listener_callback,
            odom_qos)
        self.csv_file = open('odom_data.csv', 'w', newline='')
        self.writer = csv.writer(self.csv_file)
        # Write CSV header
        #self.writer.writerow(['timestamp', 'position_x', 'position_y', 'position_z'])
        self.writer.writerow(['x', 'y', 'theta', 'stamp'])

    def listener_callback(self, msg):
        # Extracting data from the Odometry message
        timestamp_ns = Time.from_msg(msg.header.stamp).nanoseconds
        position_x = msg.pose.pose.position.x
        position_y = msg.pose.pose.position.y

        orientation_q = msg.pose.pose.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        yaw = euler_from_quaternion(orientation_list)
        theta = yaw  # Yaw angle represents theta in 2D plane

        #self.writer.writerow([timestamp, position_x, position_y, position_z])
        self.writer.writerow([position_x, position_y, yaw, timestamp_ns])


    def __del__(self):
        self.csv_file.close()

def main(args=None):
    rclpy.init(args=args)
    odom_subscriber = OdomSubscriber()
    rclpy.spin(odom_subscriber)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
