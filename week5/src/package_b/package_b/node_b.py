import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool

#!/usr/bin/env python3


class NodeB(Node):
    def __init__(self):
        super().__init__('node_b')
        self.client = self.create_client(SetBool, 'bleed')
        self.get_logger().info('Waiting for service "bleed"...')
        while rclpy.ok() and not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, retrying...')
        if not rclpy.ok():
            self.get_logger().info('Shutdown requested before service became available.')
            return

        req = SetBool.Request()
        req.data = True
        self.get_logger().info('Calling service "bleed" with data=True')
        future = self.client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        if future.result() is not None:
            res = future.result()
            self.get_logger().info(f'Service response: success={res.success}, message="{res.message}"')
        else:
            self.get_logger().error('Service call failed')


def main(args=None):
    rclpy.init(args=args)
    node = NodeB()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('KeyboardInterrupt received, shutting down.')
    finally:
        try:
            node.destroy_node()
        except Exception:
            pass
        rclpy.shutdown()


if __name__ == '__main__':
    main()