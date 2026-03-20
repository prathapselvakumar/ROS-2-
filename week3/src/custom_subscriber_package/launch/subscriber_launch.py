from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments
    topic_name_arg = DeclareLaunchArgument(
        'topic_name',
        default_value='custom_topic',
        description='Topic name to subscribe to'
    )
    
    # Create the subscriber node with parameters
    subscriber_node = Node(
        package='custom_subscriber_package',
        executable='custom_subscriber_node.py',
        name='custom_subscriber_node',
        parameters=[
            {'topic_name': LaunchConfiguration('topic_name')}
        ],
        output='screen'
    )
    
    return LaunchDescription([
        topic_name_arg,
        subscriber_node
    ])
