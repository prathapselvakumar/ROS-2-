from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # Launch ROBOT NODE
        Node(
            package='beta_pilot_pkg',
            executable='beta_pilot_node',
            name='robot_node',
            output='screen'
        ),

        # Launch CONTROLLER NODE
        Node(
            package='beta_pilot_controller_pkg',
            executable='controller_node',
            name='controller_node',
            output='screen'
        )
    ])
