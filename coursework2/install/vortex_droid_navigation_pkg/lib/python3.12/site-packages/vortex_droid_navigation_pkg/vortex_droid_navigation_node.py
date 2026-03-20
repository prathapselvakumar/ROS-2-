import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from geometry_msgs.msg import PoseWithCovarianceStamped
from nav2_msgs.action import NavigateToPose
from nav_msgs.msg import Odometry

import math
import time


class VortexOperatorNavigation(Node):

    def __init__(self):
        super().__init__('vortex_droid_navigation_node')

        self.done = False

        self.nav_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        self.init_pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )

        self.current_pose = None
        self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.get_logger().info('Waiting for Nav2 action server...')
        while not self.nav_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().info('Nav2 not ready yet...')

        self.get_logger().info('Nav2 action server available')

        self.publish_initial_pose()
        time.sleep(3.0)

        self.send_goal()

    # -------------------------------------------------

    def publish_initial_pose(self):
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()

        msg.pose.pose.position.x = 0.0
        msg.pose.pose.position.y = 0.0
        msg.pose.pose.orientation.w = 1.0

        cov = [0.0] * 36
        cov[0] = 0.25
        cov[7] = 0.25
        cov[14] = 0.25
        cov[35] = 0.068

        msg.pose.covariance = cov

        self.init_pose_pub.publish(msg)
        self.get_logger().info('Initial pose published')

    # -------------------------------------------------

    def send_goal(self):
        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()

        self.goal_x = 22.0
        self.goal_y = -7.2

        goal.pose.pose.position.x = self.goal_x
        goal.pose.pose.position.y = self.goal_y
        goal.pose.pose.orientation.w = 1.0

        self.start_time = time.time()
        self.get_logger().info('Sending navigation goal')

        self.nav_client.send_goal_async(goal).add_done_callback(
            self.goal_response_callback
        )

    # -------------------------------------------------

    def goal_response_callback(self, future):
        self.goal_handle = future.result()

        if not self.goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            self.done = True
            return

        self.get_logger().info('Goal accepted')
        self.goal_handle.get_result_async().add_done_callback(
            self.result_callback
        )

    # -------------------------------------------------

    def result_callback(self, future):
        elapsed = time.time() - self.start_time
        self.get_logger().info('Navigation finished')

        if self.current_pose is None:
            self.get_logger().error('No odometry received')
            self.done = True
            return

        dx = self.current_pose[0] - self.goal_x
        dy = self.current_pose[1] - self.goal_y
        dist = math.sqrt(dx * dx + dy * dy)

        self.get_logger().info(
            f'Final pose: x={self.current_pose[0]:.2f}, '
            f'y={self.current_pose[1]:.2f}'
        )

        if elapsed <= 60.0 and dist <= 0.5:
            self.get_logger().info('✅ SUCCESS: reached goal within 60s and 0.5 m')
        else:
            self.get_logger().error('❌ FAILED: timeout or outside tolerance')

        self.done = True

    # -------------------------------------------------

    def odom_callback(self, msg):
        self.current_pose = (
            msg.pose.pose.position.x,
            msg.pose.pose.position.y
        )


def main(args=None):
    try:
        rclpy.init(args=args)
        node = VortexOperatorNavigation()

        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.1)

        node.get_logger().info('Node finished cleanly')

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
