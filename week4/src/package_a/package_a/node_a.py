import rclpy
from rclpy.node import Node
from example_interfaces.msg import UInt32


class NodeA(Node):
    def __init__(self):
        super().__init__('node_a')
        self.publisher_ = self.create_publisher(UInt32, 'bleed', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.counter = 0

    def timer_callback(self):
        msg = UInt32()
        msg.data = self.counter
        self.publisher_.publish(msg)
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = NodeA()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
