from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='beta_pilot_controller_pkg',
            executable='beta_pilot_controller_node',
            name='controller_node',
            output='screen'
        )
    ])
