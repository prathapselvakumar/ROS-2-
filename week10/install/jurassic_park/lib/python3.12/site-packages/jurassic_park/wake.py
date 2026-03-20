import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from action_msgs.msg import GoalStatus

class Wake(Node):
    def __init__(self):
        super().__init__('wake')
        self.publisher_ = self.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
        self.nav_to_pose_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        self.timer = self.create_timer(1.0, self.publish_initial_pose)
        self.get_logger().info('Jurassic Park is waking up!')
        self.pose_published = False
        self.return_goal_sent = False

    def publish_initial_pose(self):
        if not self.pose_published:
            msg = PoseWithCovarianceStamped()
            msg.header.frame_id = 'map'
            msg.header.stamp = self.get_clock().now().to_msg()
            
            # Initial pose at (-2.0, -0.5)
            msg.pose.pose.position.x = -2.0
            msg.pose.pose.position.y = -0.5
            msg.pose.pose.position.z = 0.01
            msg.pose.pose.orientation.w = 1.0
            
            # Add covariance (standard AMCL values)
            msg.pose.covariance = [
                0.25, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.25, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                0.0, 0.0, 0.0, 0.0, 0.0, 0.06853891945200942
            ]
            
            self.publisher_.publish(msg)
            self.get_logger().info('Published initial pose')
            self.pose_published = True
            self.timer.cancel()
            
            # Wait a bit for AMCL to process the initial pose
            self.goal_timer = self.create_timer(2.0, self.send_goal_timer_callback)

    def send_goal_timer_callback(self):
        # Cancel this timer so it only runs once
        if hasattr(self, 'goal_timer'):
            self.goal_timer.cancel()
        
        # Send navigation goal
        self.send_goal()

    def send_goal(self):
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        # Goal pose at least 2m away from (-2.0, -0.5)
        # Setting to (-1.5, 1.5) which is > 2.0m away (2.06m)
        goal_msg.pose.pose.position.x = -1.5
        goal_msg.pose.pose.position.y = 1.5
        goal_msg.pose.pose.position.z = 0.0
        goal_msg.pose.pose.orientation.w = 1.0

        self.get_logger().info('Waiting for action server...')
        self.nav_to_pose_client.wait_for_server()
        
        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self.nav_to_pose_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        wrapped_result = future.result()
        status = wrapped_result.status
        result = wrapped_result.result
        
        self.get_logger().info('Result status: {0}'.format(status))
        
        if status == GoalStatus.STATUS_SUCCEEDED:
            if not self.return_goal_sent:
                self.get_logger().info('First goal reached successfully. Returning to initial pose...')
                self.send_return_goal()
            else:
                self.get_logger().info('Returned to initial pose. Mission complete!')
        else:
            self.get_logger().info('Navigation failed with status: {0}'.format(status))

    def send_return_goal(self):
        self.return_goal_sent = True
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        
        # Return to initial pose (-2.0, -0.5)
        # Adjusting slightly to (-1.5, -0.5) to ensure it's reachable
        goal_msg.pose.pose.position.x = -1.5
        goal_msg.pose.pose.position.y = -0.5
        goal_msg.pose.pose.position.z = 0.01
        goal_msg.pose.pose.orientation.w = 1.0

        self.get_logger().info('Sending return goal request...')
        self._send_goal_future = self.nav_to_pose_client.send_goal_async(goal_msg)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

def main(args=None):
    rclpy.init(args=args)
    node = Wake()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    

if __name__ == '__main__':
    main()
