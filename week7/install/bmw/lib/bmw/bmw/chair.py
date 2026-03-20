import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from sfr_ca7_interface_package.action import MoveIn1D


class ChairNode(Node):

    def __init__(self):
        super().__init__('chair')
        self.internal_value = 0.0
        self._action_server = ActionServer(
            self,
            MoveIn1D,
            'action',
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup())

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        goal_value = goal_handle.request.target_position
        result = MoveIn1D.Result()
        
        for i in range(20):
            self.internal_value += goal_value / 20.0
            self.get_logger().info(f'Iteration {i+1}: internal_value = {self.internal_value}')
        
        result.final_position = self.internal_value
        
        if abs(self.internal_value - goal_value) <= 0.01:
            self.get_logger().info(f'Goal succeeded: |{self.internal_value} - {goal_value}| <= 0.01')
            goal_handle.succeed()
        else:
            self.get_logger().info(f'Goal failed: |{self.internal_value} - {goal_value}| > 0.01')
            goal_handle.abort()
        
        return result


def main(args=None):
    rclpy.init(args=args)
    node = ChairNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
