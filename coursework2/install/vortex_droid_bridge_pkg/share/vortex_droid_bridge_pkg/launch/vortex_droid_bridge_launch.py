from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # 1) ROS2 -> Gazebo (cmd_vel)
    cmd_vel_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/box/cmd_vel@geometry_msgs/msg/Twist@ignition.msgs.Twist'
        ],
        output='screen'
    )

    # 2) Gazebo -> ROS2 (box pose to /tf)
    box_pose_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/box/pose@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V'
        ],
        output='screen'
    )

    # 3) Gazebo -> ROS2 (target_0 pose to /tf)
    t0_pose_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/target_0/pose@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V'
        ],
        output='screen'
    )

    # 4) Gazebo -> ROS2 (target_1 pose to /tf)
    t1_pose_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/model/target_1/pose@tf2_msgs/msg/TFMessage@ignition.msgs.Pose_V'
        ],
        output='screen'
    )

    return LaunchDescription([
        cmd_vel_bridge,
        box_pose_bridge,
        t0_pose_bridge,
        t1_pose_bridge,
    ])
