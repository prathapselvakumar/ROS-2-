#!/usr/bin/env python3.12

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class CustomPublisherNode(Node):
    def __init__(self):
        super().__init__('custom_publisher_node')
        
        # Declare parameters
        self.declare_parameter('timer_frequency', 1.0)
        self.declare_parameter('topic_name', 'custom_topic')
        self.declare_parameter('message_content', 'custom_string')
        
        # Get parameters
        timer_frequency = self.get_parameter('timer_frequency').value
        self.topic_name = self.get_parameter('topic_name').value
        self.message_content = self.get_parameter('message_content').value
        
        # Create publisher for custom_topic with String message type
        self.publisher_ = self.create_publisher(
            String,
            self.topic_name,
            10
        )
        
        # Create a timer to publish messages at specified frequency
        timer_period = 1.0 / timer_frequency  # Convert frequency to period
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.get_logger().info(f'Custom Publisher Node started')
        self.get_logger().info(f'Publishing to topic: {self.topic_name}')
        self.get_logger().info(f'Timer frequency: {timer_frequency} Hz')
    
    def timer_callback(self):
        msg = String()
        msg.data = self.message_content
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = CustomPublisherNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
