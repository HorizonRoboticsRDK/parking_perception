# Copyright (c) 2022，Horizon Robotics.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from launch import LaunchDescription
from launch_ros.actions import Node

from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from ament_index_python import get_package_share_directory
from ament_index_python.packages import get_package_prefix


def generate_launch_description():
    web_service_launch_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('websocket'),
                'launch/hobot_websocket_service.launch.py'))
    )

    return LaunchDescription([
        # 启动图片发布pkg
        Node(
            package='mipi_cam',
            executable='mipi_cam',
            output='screen',
            parameters=[
                {"out_format": "nv12"},
                {"image_width": 640},
                {"image_height": 320},
                {"io_method": "shared_mem"},
                {"video_device": "GC4663"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),
        # 启动jpeg图片编码&发布pkg
        Node(
            package='hobot_codec',
            executable='hobot_codec_republish',
            output='screen',
            parameters=[
                {"channel": 1},
                {"in_mode": "shared_mem"},
                {"in_format": "nv12"},
                {"out_mode": "ros"},
                {"out_format": "jpeg"},
                {"sub_topic": "/hbmem_img"},
                {"pub_topic": "/image_jpeg"}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        ),
        # 启动单目自动泊车检测
        Node(
            package='parking_perception',
            executable='parking_perception',
            output='screen',
            parameters=[
                {"feed_image": ""},
                {"ai_msg_pub_topic_name": "ai_msg_parking_perception"},
                {"dump_render_img": 1}
            ],
            arguments=['--ros-args', '--log-level', 'info']
        ),
        # 启动web展示pkg
        Node(
            package='websocket',
            executable='websocket',
            output='screen',
            parameters=[
                {"image_topic": "/image_jpeg"},
                {"image_type": "mjpeg"},
                {"smart_topic": "/hobot_parking_perception"},
                {"only_show_image": True}
            ],
            arguments=['--ros-args', '--log-level', 'error']
        )
    ])