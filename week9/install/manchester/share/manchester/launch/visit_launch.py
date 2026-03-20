from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Generate launch description for ros_gz_bridge nodes.
    
    Creates three bridges:
    1. Bidirectional bridge for /world/lidar_sensor/light_config
    2. Gazebo->ROS2 bridge for /gui/camera/pose
    3. Gazebo->ROS2 bridge for /depth_camera
    """
    
    # Bridge 1: Bidirectional bridge for light_config
    # Using @ for bidirectional communication
    bridge_light_config = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/world/lidar_sensor/light_config@ros_gz_interfaces/msg/Light@gz.msgs.Light'
        ],
        output='screen'
    )
    
    # Bridge 2: Gazebo to ROS2 bridge for camera pose
    # Using [ for Gazebo->ROS2 direction
    bridge_camera_pose = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/gui/camera/pose@geometry_msgs/msg/Pose[gz.msgs.Pose'
        ],
        output='screen'
    )
    
    # Bridge 3: Gazebo to ROS2 bridge for depth camera
    # Using [ for Gazebo->ROS2 direction
    bridge_depth_camera = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/depth_camera@sensor_msgs/msg/Image[gz.msgs.Image'
        ],
        output='screen'
    )
    
    return LaunchDescription([
        bridge_light_config,
        bridge_camera_pose,
        bridge_depth_camera,
    ])
