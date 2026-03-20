import rclpy
from rclpy.node import Node
import math
from rclpy.qos import QoSProfile

from sfr_coursework1_interface_package.msg import WheelAngularVelocities, TaskSpacePose
from sfr_coursework1_interface_package.srv import TurnRobotOn, TurnRobotOff


class ControllerNode(Node):
    def __init__(self):
        super().__init__("controller_node")

        # Assigned from coursework spreadsheet
        self.desired_angle_deg = 124.0
        self.desired_angle_rad = math.radians(self.desired_angle_deg)

        # Robot physical parameters
        self.r = 0.09
        self.l = 0.28

        # Robot state
        self.current_phi = 0.0
        self.current_x = 0.0
        self.current_y = 0.0

        self.rotation_done = False
        self.translation_done = False

        self.start_x = None
        self.start_y = None

        qos = QoSProfile(depth=10)

        # Publisher for wheel angular velocities
        self.pub = self.create_publisher(
            WheelAngularVelocities,
            "robot/wheel_angular_velocities",
            qos
        )

        # Subscriber for pose feedback
        self.create_subscription(
            TaskSpacePose,
            "robot/task_space_pose",
            self.pose_callback,
            qos
        )

        # Service clients
        self.on_client = self.create_client(TurnRobotOn, "robot/turn_robot_on")
        self.off_client = self.create_client(TurnRobotOff, "robot/turn_robot_off")

        self.wait_for_services()
        self.turn_robot_on()

        # Control loop timer
        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info(f"Controller node started. Target angle = {self.desired_angle_deg}°")


    # -------------------------------------------------------
    def wait_for_services(self):
        while not self.on_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for turn_robot_on service...")

        while not self.off_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info("Waiting for turn_robot_off service...")


    # -------------------------------------------------------
    def turn_robot_on(self):
        req = TurnRobotOn.Request()
        future = self.on_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        self.get_logger().info("Robot turned ON by controller.")


    def turn_robot_off(self):
        req = TurnRobotOff.Request()
        future = self.off_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        self.get_logger().info("Robot turned OFF by controller.")


    # -------------------------------------------------------
    def pose_callback(self, msg):
        self.current_x = msg.x
        self.current_y = msg.y
        self.current_phi = msg.phi_z


    # -------------------------------------------------------
    def control_loop(self):

        # ============================
        # PHASE 1 — ROTATE ROBOT
        # ============================
        if not self.rotation_done:

            self.get_logger().info(
                f"Rotating robot toward {self.desired_angle_deg} degrees... (current={math.degrees(self.current_phi):.2f})"
            )

            if self.current_phi >= self.desired_angle_rad:
                # STOP rotation
                msg = WheelAngularVelocities()
                msg.left_wheel_angular_velocity = 0.0
                msg.right_wheel_angular_velocity = 0.0
                self.pub.publish(msg)

                self.rotation_done = True
                self.start_x = self.current_x
                self.start_y = self.current_y

                self.get_logger().info("Rotation complete. Starting translation forward 1 meter.")
                return

            # Continue rotating
            omega = 0.5  # rad/s rotation speed
            v_r = (self.l * omega) / 2
            v_l = -v_r

            msg = WheelAngularVelocities()
            msg.left_wheel_angular_velocity = v_l / self.r
            msg.right_wheel_angular_velocity = v_r / self.r
            self.pub.publish(msg)
            return

        # ============================
        # PHASE 2 — MOVE FORWARD 1 METER
        # ============================
        if not self.translation_done:

            dx = self.current_x - self.start_x
            dy = self.current_y - self.start_y
            distance = math.sqrt(dx*dx + dy*dy)

            self.get_logger().info(f"Moving forward... Distance = {distance:.3f} m")

            if distance >= 1.0:
                # STOP
                msg = WheelAngularVelocities()
                msg.left_wheel_angular_velocity = 0.0
                msg.right_wheel_angular_velocity = 0.0
                self.pub.publish(msg)

                self.get_logger().info("Target distance achieved (1.000 m). Stopping robot.")

                self.translation_done = True
                self.turn_robot_off()
                self.get_logger().info("Translation complete. Controller stopping.")
                self.destroy_timer(self.timer)
                return

            # Continue straight motion
            v = 0.1  # m/s

            msg = WheelAngularVelocities()
            msg.left_wheel_angular_velocity = v / self.r
            msg.right_wheel_angular_velocity = v / self.r
            self.pub.publish(msg)


# -------------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = ControllerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Keyboard interrupt received. Shutting down cleanly.")
   


if __name__ == "__main__":
    main()
