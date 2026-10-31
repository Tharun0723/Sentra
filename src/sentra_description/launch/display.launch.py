from launch import LaunchDescription
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    """Show the SENTRA URDF in RViz with a joint-state GUI for the drive wheels."""
    pkg_share = FindPackageShare('sentra_description')
    urdf_file = PathJoinSubstitution([pkg_share, 'urdf', 'sentra.urdf.xacro'])
    rviz_file = PathJoinSubstitution([pkg_share, 'rviz', 'display.rviz'])

    # ParameterValue(..., value_type=str) stops ROS 2 from parsing the URDF as YAML.
    robot_description = ParameterValue(Command(['xacro ', urdf_file]), value_type=str)

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_file],
        ),
    ])
