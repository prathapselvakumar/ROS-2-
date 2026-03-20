#!/usr/bin/env python3.12

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class CustomSubscriberNode(Node):
    def __init__(self):
        super().__init__('custom_subscriber_node')
        
        # Declare parameters
        self.declare_parameter('topic_name', 'custom_topic')
        
        # Get parameters
        topic_name = self.get_parameter('topic_name').value
        
        # Create subscription to custom_topic with String message type
        self.subscription = self.create_subscription(
            String,
            topic_name,
            self.listener_callback,
            10
        )
        
        self.get_logger().info('Custom Subscriber Node started')
        self.get_logger().info(f'Subscribed to topic: {topic_name}')
    
    def listener_callback(self, msg):
        self.get_logger().info(f'Received: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    node = CustomSubscriberNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
