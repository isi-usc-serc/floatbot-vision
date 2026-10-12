from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import ComposableNodeContainer
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
                'frame_id': camera_ns
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
            name = 'apriltag',
            namespace = camera_ns,
            parameters = [
                PathJoinSubstitution([FindPackageShare('floatbot_vision'), 'cfg', 'tags_floatbot.yaml'])
            ],
            remappings = [
                ('detections', 'tags')
            ],
            extra_arguments = [{
                'use_intra_process_comms': True
            }]
        )
    ]

    # create vision pipeline container
    ld.add_action(
        ComposableNodeContainer(
            name='vision_pipeline',
            package='rclcpp_components',
            namespace=camera_ns,
            executable='component_container',
            composable_node_descriptions=vision_nodes
        )
    )
    
    return ld