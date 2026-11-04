


import os

from launch import LaunchDescription
from launch.actions import (
    IncludeLaunchDescription,
    RegisterEventHandler,
    TimerAction,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # Package directories
    gazebo_share = get_package_share_directory('sentra_gazebo')
    description_share = get_package_share_directory('sentra_description')
    ros_gz_share = get_package_share_directory('ros_gz_sim')

    # Simulation files
    world_file = os.path.join(
        gazebo_share, 'worlds', 'empty.sdf'
    )

    robot_xacro = os.path.join(
        description_share, 'urdf', 'sentra_sim.urdf.xacro'
    )

    # Generate robot description
    robot_description = ParameterValue(
        Command([
            FindExecutable(name='xacro'),
            ' ',
            robot_xacro
        ]),
        value_type=str
    )

    # Publish robot description and TF
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }],
        output='screen'
    )

    # Start Gazebo Harmonic
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                ros_gz_share,
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={
            'gz_args': f'-r {world_file}'
        }.items()
    )

    # Bridge Gazebo clock to ROS 2
    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen'
    )

    # Spawn SENTRA
    spawn_sentra = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-world', 'sentra_world',
            '-topic', '/robot_description',
            '-name', 'sentra',
            '-z', '0.02'
        ],
        output='screen'
    )

    # Load joint state broadcaster
    joint_state_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager',
            '--controller-manager-timeout',
            '60'
        ],
        output='screen'
    )

    # Load differential drive controller
    diff_drive_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_base_controller',
            '--controller-manager',
            '/controller_manager',
            '--controller-manager-timeout',
            '60'
        ],
        output='screen'
    )

    return LaunchDescription([

        robot_state_publisher,

        gazebo,

        clock_bridge,

        # Initial wait for Gazebo to start
        TimerAction(
            period=5.0,
            actions=[spawn_sentra]
        ),

        # Load joint states after successful robot spawning
        RegisterEventHandler(
            OnProcessExit(
                target_action=spawn_sentra,
                on_exit=lambda event, context: (
                    [joint_state_spawner]
                    if event.returncode == 0 else []
                )
            )
        ),

        # Load drive controller after joint states
        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_spawner,
                on_exit=lambda event, context: (
                    [diff_drive_spawner]
                    if event.returncode == 0 else []
                )
            )
        ),

    ])
