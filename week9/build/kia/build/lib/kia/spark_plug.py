#!/usr/bin/env python3
"""
spark_plug node - Sets the pose of Construction Cone entity in Gazebo.

This node sends a service request to /world/lidar_sensor/set_pose to move
the "Construction Cone" entity to position (0, 0, 10) with rotation w=1.
"""

import rclpy
from rclpy.node import Node
from ros_gz_interfaces.srv import SetEntityPose
from geometry_msgs.msg import Pose, Point, Quaternion


class SparkPlugNode(Node):
    """Node that sets the pose of Construction Cone in Gazebo."""

    def __init__(self):
        super().__init__('spark_plug')
        
        # Create service client
        self.client = self.create_client(
            SetEntityPose,
            '/world/lidar_sensor/set_pose'
        )
        
        self.get_logger().info('spark_plug node started')
        
        # Wait for service to be available
        self.get_logger().info('Waiting for service /world/lidar_sensor/set_pose...')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting...')
        
        self.get_logger().info('Service available, sending request...')
        self.send_request()

    def send_request(self):
        """Send service request to set Construction Cone pose."""
        # Create the request
        request = SetEntityPose.Request()
        request.entity.name = 'Construction Cone'
        
        # Set the pose
        request.pose.position.x = 0.0
        request.pose.position.y = 0.0
        request.pose.position.z = 10.0
        
        # Set rotation quaternion (w=1 means no rotation)
        request.pose.orientation.x = 0.0
        request.pose.orientation.y = 0.0
        request.pose.orientation.z = 0.0
        request.pose.orientation.w = 1.0
        
        # Send the request asynchronously
        self.future = self.client.call_async(request)
        self.future.add_done_callback(self.response_callback)

    def response_callback(self, future):
        """Handle the service response."""
        try:
            response = future.result()
            if response.success:
                self.get_logger().info(
                    'Successfully set Construction Cone pose to (0, 0, 10)'
                )
            else:
                self.get_logger().error(
                    'Failed to set Construction Cone pose'
                )
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
        finally:
            # Shutdown cleanly after service call completes
            self.get_logger().info('Shutting down spark_plug node')
            rclpy.shutdown()


def main(args=None):
    """Main entry point for the spark_plug node."""
    rclpy.init(args=args)
    
    try:
        node = SparkPlugNode()
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('\nKeyboardInterrupt received, shutting down cleanly...')
    except Exception as e:
        print(f'Error: {e}')
    finally:
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
