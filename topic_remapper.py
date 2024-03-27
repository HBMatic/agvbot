#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TopicRemapper(Node):
    def __init__(self):
        super().__init__('topic_remapper')

        # Source topic subscriber
        self.source_subscriber = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.source_callback,
            10
        )

        # Destination topic publisher
        self.destination_publisher = self.create_publisher(
            Twist,
            '/diff_cont/cmd_vel_unstamped',
            10
        )

    def source_callback(self, msg):
        # Callback function for the source topic
        self.get_logger().info(f"Received from source: linear.x={msg.linear.x}, angular.z={msg.angular.z}")

        # Publish the received message to the destination topic
        destination_msg = Twist()
        destination_msg.linear.x = msg.linear.x
        destination_msg.angular.z = msg.angular.z
        self.destination_publisher.publish(destination_msg)

def main(args=None):
    rclpy.init(args=args)

    topic_remapper = TopicRemapper()

    try:
        while rclpy.ok():
            rclpy.spin_once(topic_remapper, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass

    topic_remapper.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

