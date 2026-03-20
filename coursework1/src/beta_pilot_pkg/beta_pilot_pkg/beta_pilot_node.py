import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
import math

from sfr_coursework1_interface_package.msg import WheelAngularVelocities, TaskSpacePose
from sfr_coursework1_interface_package.srv import TurnRobotOn, TurnRobotOff


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
