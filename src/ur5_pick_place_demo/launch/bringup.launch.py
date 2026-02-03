from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

def generate_launch_description():
    pkg_share = get_package_share_directory('ur5_pick_place_demo')
    urdf_path = os.path.join(pkg_share, 'urdf', 'ur5_simple.urdf')

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': ParameterValue(
                Command(['cat ', urdf_path]),
                value_type=str
            )
        }],
    )


    republisher_node = Node(
        package='ur5_pick_place_demo',
        executable='republish_joint_states',
        name='republish_joint_states',
        output='screen',
    )

    demo_node = Node(
        package='ur5_pick_place_demo',
        executable='pick_place_demo',
        name='pick_place_demo',
        output='screen',
    )

    object_node = Node(
        package='ur5_pick_place_demo',
        executable='scene_object_publisher',
        name='scene_object_publisher',
        output='screen',
    )


    return LaunchDescription([
        robot_state_publisher_node,
        republisher_node,
        demo_node,
        object_node
    ])
