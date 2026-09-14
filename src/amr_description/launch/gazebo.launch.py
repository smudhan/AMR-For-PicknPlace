# import os

# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource
# from launch_ros.actions import Node
# from launch.substitutions import Command
# from launch_ros.parameter_descriptions import ParameterValue
# from ament_index_python.packages import get_package_share_directory


# def generate_launch_description():

#     pkg_share = get_package_share_directory('amr_description')

#     xacro_file = os.path.join(
#         pkg_share,
#         'urdf',
#         'amr.urdf.xacro'
#     )

#     world_file = os.path.join(
#         pkg_share,
#         'worlds',
#         'empty.world'
#     )

#     robot_description = ParameterValue(
#         Command(['xacro ', xacro_file]),
#         value_type=str
#     )

#     gazebo_launch = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource(
#             os.path.join(
#                 get_package_share_directory('gazebo_ros'),
#                 'launch',
#                 'gazebo.launch.py'
#             )
#         ),
#         launch_arguments={
#             'world': world_file
#         }.items()
#     )

#     robot_state_publisher = Node(
#         package='robot_state_publisher',
#         executable='robot_state_publisher',
#         name='robot_state_publisher',
#         parameters=[
#             {
#                 'robot_description': robot_description
#             }
#         ]
#     )

#     joint_state_publisher = Node(
#         package='joint_state_publisher',
#         executable='joint_state_publisher',
#         name='joint_state_publisher'
#     )

#     spawn_robot = Node(
#         package='gazebo_ros',
#         executable='spawn_entity.py',
#         name='spawn_amr',
#         arguments=[
#             '-topic',
#             'robot_description',
#             '-entity',
#             'amr'
#         ],
#         output='screen'
#     )

#     return LaunchDescription([
#         gazebo_launch,
#         robot_state_publisher,
#         joint_state_publisher,
#         spawn_robot
#     ])

import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit

from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_share = get_package_share_directory('amr_description')

    xacro_file = os.path.join(
        pkg_share,
        'urdf',
        'amr.urdf.xacro'
    )

    world_file = os.path.join(
        pkg_share,
        'worlds',
        'empty.world'
    )

    controllers_file = os.path.join(
        pkg_share,
        'config',
        'controllers.yaml'
    )

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]),
        value_type=str
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            )
        ),
        launch_arguments={
            'world': world_file
        }.items()
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_description
            }
        ]
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_amr',
        arguments=[
            '-topic',
            'robot_description',
            '-entity',
            'amr'
        ],
        output='screen'
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    diff_drive_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'diff_drive_controller',
            '--controller-manager',
            '/controller_manager',
            '--ros-args',
            '-r', 'cmd_vel_unstamped:=/cmd_vel',
            '-r', 'odom:=/odom'
        ],
        output='screen'
    )

    return LaunchDescription([

        gazebo_launch,

        robot_state_publisher,

        spawn_robot,

        RegisterEventHandler(
            OnProcessExit(
                target_action=spawn_robot,
                on_exit=[
                    joint_state_broadcaster_spawner,
                    diff_drive_controller_spawner
                ]
            )
        ),

    ])