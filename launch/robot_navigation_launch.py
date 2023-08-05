import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

	# Initialise paths to files and folders
	pkg_share = FindPackageShare(package='robot_navigation').find('robot_navigation')
	default_model_path = os.path.join(pkg_share, 'models/robot_model.urdf')
	default_rviz_config_path = os.path.join(pkg_share, 'rviz/urdf_config.rviz')
	
	# Declaring launch configurations
	model = LaunchConfiguration('model')
	rviz_config = LaunchConfiguration('rviz_config')

	# Declaring the launch arguments
	model_cmd = DeclareLaunchArgument(
		name='model',
		default_value=default_model_path,
		description='Absolute path to the robot urdf file'
	)

	rviz_config_cmd = DeclareLaunchArgument(
		name='rviz_config',
		default_value=default_rviz_config_path,
		description='Absolute path to rviz config file'
	)
	
	# Declaring the actions to be run
	robot_state_publisher_node = Node(
		package='robot_state_publisher',
		executable='robot_state_publisher',
		parameters=[{'robot_description': Command(['xacro ', model])}]
	)
	
	joint_state_publisher_node = Node(
		package='joint_state_publisher',
		executable='joint_state_publisher',
		name='joint_state_publisher'
	)

	rviz_node = Node(
		package='rviz2',
		executable='rviz2',
		name='rviz2',
		output='screen',
		arguments=['-d', rviz_config]
	)
	
	# Launch the ROS2 Navigation Stack

	
	# Create a launch description
	ld = LaunchDescription()

	ld.add_action(model_cmd)
	ld.add_action(rviz_config_cmd)
	ld.add_action(joint_state_publisher_node)
	ld.add_action(robot_state_publisher_node)
	ld.add_action(rviz_node)

	return ld
