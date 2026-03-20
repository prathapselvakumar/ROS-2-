import rclpy
from rclpy.node import Node
from example_interfaces.srv import SetBool

TEXT = "grace"        # response.message must be set to this
SERVICE_NAME = "bleed"  # service must be named "bleed"

class NodeA(Node):
    def __init__(self):
        super().__init__('brakes')
        self.srv = self.create_service(SetBool, SERVICE_NAME, self.handle_set_bool)
        self.get_logger().info(f'Service "{SERVICE_NAME}" ready')

    def handle_set_bool(self, request, response):
        response.success = True
        response.message = TEXT
        self.get_logger().info(f'Responding success={response.success} message="{response.message}"')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = NodeA()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('KeyboardInterrupt received, shutting down')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()