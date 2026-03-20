import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
import math

from sfr_coursework1_interface_package.msg import WheelAngularVelocities, TaskSpacePose
from sfr_coursework1_interface_package.srv import TurnRobotOn, TurnRobotOff
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster


class BetaPilotNode(Node):
    def __init__(self):
        super().__init__("beta_pilot_node")

        # Robot parameters (from spreadsheet)
        self.r = 0.09    # wheel radius
        self.l = 0.28    # wheel separation
        self.T = 0.1     # update rate (10 Hz)

        # State machine
        self.OFF = "OFF"
        self.ON = "ON"
        self.robot_state = self.OFF
        self.get_logger().info("Robot starting in state: OFF")

        # Wheel angular velocities
        self.omega_l = 0.0
        self.omega_r = 0.0

        # Robot pose
        self.x = 0.0
        self.y = 0.0
        self.phi = 0.0

        # Services
        self.create_service(TurnRobotOn, "robot/turn_robot_on", self.turn_robot_on_callback)
        self.create_service(TurnRobotOff, "robot/turn_robot_off", self.turn_robot_off_callback)

        # Publisher (robot pose)
        qos = QoSProfile(depth=10)
        self.pose_pub = self.create_publisher(TaskSpacePose, "robot/task_space_pose", qos)

        # Subscriber (wheel velocities)
        self.create_subscription(
            WheelAngularVelocities,
            "robot/wheel_angular_velocities",
            self.wheel_velocity_callback,
            qos
        )

        # TF Broadcaster for RViz
        self.tf_broadcaster = TransformBroadcaster(self)

        # Timer for robot motion updates
        self.create_timer(self.T, self.update_robot)

    # -------------------------------------------------------------
    # SERVICE CALLBACKS
    # -------------------------------------------------------------
    def turn_robot_on_callback(self, request, response):
        if self.robot_state == self.OFF:
            self.robot_state = self.ON
            response.success = True
            self.get_logger().info("Robot turned ON")
        else:
            response.success = False
        return response

    def turn_robot_off_callback(self, request, response):
        if self.robot_state == self.ON:
            self.robot_state = self.OFF
            response.success = True
            self.get_logger().info("Robot turned OFF")

            # Reset wheel velocities
            self.omega_l = 0.0
            self.omega_r = 0.0
        else:
            response.success = False
        return response

    # -------------------------------------------------------------
    # WHEEL VELOCITY SUBSCRIBER
    # -------------------------------------------------------------
    def wheel_velocity_callback(self, msg):
        if self.robot_state == self.OFF:
            return  # ignore commands when OFF

        # Store wheel angular velocities from message
        self.omega_l = msg.left_wheel_angular_velocity
        self.omega_r = msg.right_wheel_angular_velocity

        # Convert to linear velocity
        v_l = self.r * self.omega_l
        v_r = self.r * self.omega_r

        # Clamp: maximum 0.1 m/s
        v_l = max(-0.1, min(0.1, v_l))
        v_r = max(-0.1, min(0.1, v_r))

        # Convert back to angular velocity
        self.omega_l = v_l / self.r
        self.omega_r = v_r / self.r

    # -------------------------------------------------------------
    # ROBOT MOTION UPDATE
    # -------------------------------------------------------------
    def update_robot(self):
        if self.robot_state == self.OFF:
            return  # no movement

        # Convert wheel speeds to linear velocities
        v_l = self.r * self.omega_l
        v_r = self.r * self.omega_r

        # Differential-drive equations
        v = (v_r + v_l) / 2.0
        omega = (v_r - v_l) / self.l

        # Update pose
        self.x += v * math.cos(self.phi) * self.T
        self.y += v * math.sin(self.phi) * self.T
        self.phi += omega * self.T

        # Publish pose
        pose_msg = TaskSpacePose()
        pose_msg.x = self.x
        pose_msg.y = self.y
        pose_msg.phi_z = self.phi
        self.pose_pub.publish(pose_msg)

        # Broadcast transform (RViz visualization)
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        
        # Convert phi_z to quaternion
        q = self.quaternion_from_euler(0, 0, self.phi)
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]

        self.tf_broadcaster.sendTransform(t)

    def quaternion_from_euler(self, ai, aj, ak):
        ai /= 2.0
        aj /= 2.0
        ak /= 2.0
        ci = math.cos(ai)
        si = math.sin(ai)
        cj = math.cos(aj)
        sj = math.sin(aj)
        ck = math.cos(ak)
        sk = math.sin(ak)
        cc = ci*cj
        cs = ci*sj
        sc = si*cj
        ss = si*sj

        q = [
            (sc*ck - cs*sk),
            (sc*sk + cs*ck),
            (cc*sk - ss*ck),
            (cc*ck + ss*sk)
        ]
        return q

    # -------------------------------------------------------------
    # CLEAN SHUTDOWN
    # -------------------------------------------------------------
    def destroy(self):
        self.get_logger().info("Shutting down beta_pilot_node cleanly...")
        super().destroy_node()


# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = BetaPilotNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt received.")
    
if __name__ == "__main__":
    main()
