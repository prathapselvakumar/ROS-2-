import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class NodeB(Node):
    def __init__(self):
        super().__init__('node_b')
        self.subscription = self.create_subscription(
            String,
            'edinburgh',
            self.listener_callback,
            10)
        self.subscription

    def listener_callback(self, msg):
        self.get_logger().info(f'Received: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = NodeB()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
