from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    '''
    Generate launch description for the floatbot vision system
    '''

    # initialize launch description
    ld = LaunchDescription()

    # parameters
    camera_ns = 'camera'

    # composable nodes
    vision_nodes = [

        # camera node
        ComposableNode(
            package = 'camera_ros',
            plugin = 'camera::CameraNode',
            name = camera_ns,
            parameters = [{
                'frame_id': camera_ns,
                'width': 1280,
                'height': 720
            }],
            extra_arguments = [{
                'use_intra_process_comms': True
            }]
        ),

        # rectifier node
        ComposableNode(
            package = 'image_proc',
            plugin = 'image_proc::RectifyNode',
            name = 'rectifier',
            namespace = camera_ns,
            parameters=[{
                'image_transport': 'compressed'
            }],
            remappings = [
                ('image', 'image_raw')
            ],
            extra_arguments=[{
                'use_intra_process_coms': True
            }]
        ),

        # apriltag node
        ComposableNode(
            package = 'apriltag_ros',
            plugin = 'AprilTagNode',
            name = 'apriltag_detector',
            namespace = camera_ns,
            parameters = [
                PathJoinSubstitution([FindPackageShare('floatbot_vision'), 'cfg', 'tags_floatbot.yaml'])
            ],
            extra_arguments = [{
                'use_intra_process_comms': True
            }]
        )
    ]

    # create vision pipeline container
    ld.add_action(
        ComposableNodeContainer(
            name = 'vision_pipeline',
            package = 'rclcpp_components',
            executable = 'component_container_mt',
            namespace = camera_ns,
            composable_node_descriptions = vision_nodes
        )
    )

    # camera transform publisher
    ld.add_action(
        Node(
            package = 'tf2_ros',
            executable = 'static_transform_publisher',
            name = 'transform_publisher',
            namespace = camera_ns,
            arguments = [
                '--x', '0', '--y', '0', '--z', '2.13',
                '--yaw', '0', '--pitch', '0', '--roll', '3.14159',
                '--frame-id', 'world', '--child-frame-id', camera_ns
            ]
        )
    )

    # complete launch description
    return ld