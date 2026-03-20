import os
from ament_index_python.packages import get_package_share_directory
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
            executable='beta_pilot_controller_node',
            name='controller_node',
            output='screen'
        ),

        # Launch RVIZ
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', [os.path.join(get_package_share_directory('beta_pilot_launch_pkg'), 'rviz', 'default.rviz')]],
            output='screen'
        )
    ])
