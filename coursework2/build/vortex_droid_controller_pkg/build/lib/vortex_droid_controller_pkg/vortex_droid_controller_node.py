#!/usr/bin/env python3

import math
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse

from geometry_msgs.msg import Twist, PoseStamped
from tf2_msgs.msg import TFMessage

from sfr_coursework2_interface_package.action import DroneControl # pyright: ignore[reportMissingImports]


class VortexOperatorController(Node):

    def __init__(self):
        super().__init__('vortex_droid_controller_node')

        # Velocity command publisher
        self.cmd_pub = self.create_publisher(
            Twist,
            '/model/box/cmd_vel',
            10
        )

        # Pose from Gazebo (via bridge)
        self.pose_sub = self.create_subscription(
            TFMessage,
            '/model/box/pose',
            self.pose_callback,
            10
        )

        # Action server (TASK 2 REQUIREMENT)
        self.action_server = ActionServer(
            self,
            DroneControl,
            'vortex_droid/set_pose',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.current_pose = None
        self.get_logger().info('vortex_droid_controller_node ready')

    # -----------------------------------------------------

    def pose_callback(self, msg: TFMessage):
        if not msg.transforms:
            return

        t = msg.transforms[0]

        ps = PoseStamped()
        ps.header = t.header
        ps.pose.position.x = t.transform.translation.x
        ps.pose.position.y = t.transform.translation.y
        ps.pose.position.z = t.transform.translation.z
        ps.pose.orientation = t.transform.rotation

        self.current_pose = ps

    # -----------------------------------------------------

    def goal_callback(self, goal_request):
        self.get_logger().info('Goal accepted')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Cancel request accepted')
        return CancelResponse.ACCEPT

    # -----------------------------------------------------

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal')

        target = goal_handle.request.desired_pose
        feedback = DroneControl.Feedback()
        result = DroneControl.Result()

        # Wait for pose (max 1 sec)
        start_wait = time.time()
        while self.current_pose is None:
            if time.time() - start_wait > 1.0:
                self.get_logger().error('No pose received from Gazebo')
                result.success = False
                goal_handle.abort()
                return result
            rclpy.spin_once(self, timeout_sec=0.01)

        Kp = 1.6
        vmax = 1.6
        tolerance = 0.1        # TASK 2
        timeout = 5.0          # TASK 2

        start_time = time.time()

        while time.time() - start_time < timeout:

            curr = self.current_pose

            dx = target.pose.position.x - curr.pose.position.x
            dy = target.pose.position.y - curr.pose.position.y
            dz = target.pose.position.z - curr.pose.position.z

            dist = math.sqrt(dx*dx + dy*dy + dz*dz)

            feedback.current_pose = curr
            goal_handle.publish_feedback(feedback)

            if dist <= tolerance:
                self.cmd_pub.publish(Twist())
                result.success = True
                goal_handle.succeed()
                self.get_logger().info('Target reached within tolerance')
                return result

            cmd = Twist()
            cmd.linear.x = max(-vmax, min(vmax, Kp * dx))
            cmd.linear.y = max(-vmax, min(vmax, Kp * dy))
            cmd.linear.z = max(-vmax, min(vmax, Kp * dz))

            self.cmd_pub.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.01)

        # Timeout
        self.cmd_pub.publish(Twist())
        self.get_logger().info('Timeout — goal aborted')
        result.success = False
        goal_handle.abort()
        return result


def main(args=None):
    try:
        rclpy.init(args=args)
        node = VortexOperatorController()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
