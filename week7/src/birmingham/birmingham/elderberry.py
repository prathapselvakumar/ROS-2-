import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from sfr_coursework1_interface_package.action import MoveIn1D


class ElderberryNode(Node):

    def __init__(self):
        super().__init__('elderberry')
        self._action_client = ActionClient(self, MoveIn1D, 'action')

    def send_goal(self, value):
        try:
            goal_msg = MoveIn1D.Goal()
            goal_msg.target_position = value

            self._action_client.wait_for_server()
            self._send_goal_future = self._action_client.send_goal_async(goal_msg)
            self._send_goal_future.add_done_callback(self.goal_response_callback)
        except Exception as e:
            self.get_logger().error(f'Error sending goal: {e}')

    def goal_response_callback(self, future):
        try:
            goal_handle = future.result()
            if not goal_handle.accepted:
                self.get_logger().info('Goal rejected :(')
                return

            self.get_logger().info('Goal accepted :)')
            self._get_result_future = goal_handle.get_result_async()
            self._get_result_future.add_done_callback(self.get_result_callback)
        except Exception as e:
            self.get_logger().error(f'Error in goal response: {e}')

    def get_result_callback(self, future):
        try:
            result = future.result().result
            self.get_logger().info('Result received')
        except Exception as e:
            self.get_logger().error(f'Error getting result: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ElderberryNode()
    
    node.send_goal(-0.08)
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

       


if __name__ == '__main__':
    main()
