from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    pkg_share = get_package_share_directory('amr_description')

    nav2_params = os.path.join(
        pkg_share,
        'config',
        'nav2_params.yaml'
    )


    return LaunchDescription([


        # Planner
        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[nav2_params]
        ),

        # Controller
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[nav2_params],
            remappings=[
                ('cmd_vel', '/diff_drive_controller/cmd_vel_unstamped'),
            ],
        ),

        # Behavior Tree navigator
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[nav2_params]
        ),

        # Behavior server
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            output='screen',
            parameters=[nav2_params]
        ),

        # Waypoint follower
        Node(
            package='nav2_waypoint_follower',
            executable='waypoint_follower',
            name='waypoint_follower',
            output='screen',
            parameters=[nav2_params]
        ),

        # Lifecycle manager
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[
                nav2_params,
                {
                    'autostart': True,
                    'node_names': [
                        'planner_server',
                        'controller_server',
                        'bt_navigator',
                        'behavior_server',
                        'waypoint_follower'
                    ]
                }
            ]
        ),
    ])