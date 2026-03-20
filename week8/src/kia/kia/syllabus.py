#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped

class SyllabusNode(Node):
    def __init__(self):
        super().__init__('syllabus')
        
        # Create TransformBroadcaster
        self.br = TransformBroadcaster(self)
        
        # Parameters
        self.speed = 0.55  # m/s
        self.axis = 'y'  # axis of motion
        self.period = 0.01  # seconds
        self.displacement = self.speed * self.period  # displacement per period
        
        # Position tracking (starts at origin)
        self.position = {'x': 0.0, 'y': 0.0, 'z': 0.0}
        
        # Create a timer that fires every 0.01 seconds (100 Hz)
        self.timer = self.create_timer(self.period, self.timer_callback)
        
        self.get_logger().info(f'Syllabus node started - Speed: {self.speed} m/s, Axis: {self.axis}')
    
    def timer_callback(self):
        # Update position based on speed and axis
        self.position[self.axis] += self.displacement
        
        # Get current time from the node's clock
        now = self.get_clock().now()
        
        # Create a TransformStamped message
        t = TransformStamped()
        
        # Set the timestamp
        t.header.stamp = now.to_msg()
        
        # Set frame IDs
        t.header.frame_id = 'fusion_droid'
        t.child_frame_id = 'robo_walker'
        
        # Set translation based on current position
        t.transform.translation.x = self.position['x']
        t.transform.translation.y = self.position['y']
        t.transform.translation.z = self.position['z']
        
        # Set rotation (identity quaternion)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0
        
        # Log the transformation
        self.get_logger().info(
            f'Transform: position=[x={self.position["x"]:.4f}, y={self.position["y"]:.4f}, z={self.position["z"]:.4f}], '
            f'rotation=[x=0.0, y=0.0, z=0.0, w=1.0]'
        )
        
        # Broadcast the transformation
        self.br.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = SyllabusNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    

if __name__ == '__main__':
    main()
