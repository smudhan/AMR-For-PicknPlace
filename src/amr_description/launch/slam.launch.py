import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    pkg_share = get_package_share_directory('amr_description')

    slam_config = os.path.join(
        pkg_share,
        'config',
        'slam_toolbox.yaml'
    )

    slam_toolbox = Node(
        package='slam_toolbox',
        executable='sync_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[slam_config],
    )

    return LaunchDescription([
        slam_toolbox
    ])