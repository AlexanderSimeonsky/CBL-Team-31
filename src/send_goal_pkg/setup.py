import os
from setuptools import setup
from glob import glob

package_name = 'send_goal_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),  # Include launch files here
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntuhost',
    maintainer_email='ubuntuhost@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'send_goal = send_goal_pkg.send_goal:main',
            'publish_goal = send_goal_pkg.publish_goal:main',
            'initial_pose = send_goal_pkg.initial_pose:main',
            'get_turtlebot_pose = send_goal_pkg.get_turtlebot_pose:main',
        ],
    },
)

