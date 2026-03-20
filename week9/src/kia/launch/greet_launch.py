from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Generate launch description for service bridge and spark_plug node.
    
    Creates:
    1. Bidirectional service bridge for /world/lidar_sensor/set_pose
    2. spark_plug node that calls the service
    """
    
    # Service bridge: Bidirectional bridge for set_pose service
    # Using @ for bidirectional communication
    service_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/world/lidar_sensor/set_pose@ros_gz_interfaces/srv/SetEntityPose'
        ],
        output='screen'
    )
    
    # spark_plug node that will call the service
    spark_plug_node = Node(
        package='kia',
        executable='spark_plug',
        name='spark_plug',
        output='screen'
    )
    
    return LaunchDescription([
        service_bridge,
        spark_plug_node,
    ])
