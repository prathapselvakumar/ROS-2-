from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments
    timer_frequency_arg = DeclareLaunchArgument(
        'timer_frequency',
        default_value='1.0',
        description='Timer frequency in Hz for publishing messages'
    )
    
    topic_name_arg = DeclareLaunchArgument(
        'topic_name',
        default_value='custom_topic',
        description='Topic name to publish to'
    )
    
    message_content_arg = DeclareLaunchArgument(
        'message_content',
        default_value='custom_string',
        description='Content of the message to publish'
    )
    
    # Create the publisher node with parameters
    publisher_node = Node(
        package='custom_publisher_package',
        executable='custom_publisher_node.py',
        name='custom_publisher_node',
        parameters=[
            {'timer_frequency': LaunchConfiguration('timer_frequency')},
            {'topic_name': LaunchConfiguration('topic_name')},
            {'message_content': LaunchConfiguration('message_content')}
        ],
        output='screen'
    )
    
    return LaunchDescription([
        timer_frequency_arg,
        topic_name_arg,
        message_content_arg,
        publisher_node
    ])
